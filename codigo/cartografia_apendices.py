# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/base_regional/municipios_vizinhos_cache.geojson | gp.read_file.
# Entrada: E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.svg | svg_path.read_text.
# Campos/chaves em config.DIRS: out.
# Campos/chaves em v: name.
# Campos/chaves em surface: cmap, limits, norm, values, x, y.
# Campos/chaves em opts: ticklabels.
# Campos/chaves em s: cmap, norm, ticks, values.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.{ext} | fig.savefig.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.svg | svg_path.write_text.
# Campos/chaves gerados em surface: _bar_position.
# Campos/chaves gerados em handles: missing, peak.
# CÓDIGO DO PROCESSAMENTO

"""Cartografia em SIRGAS 2000 com escala geodésica e contexto municipal."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_congonhas import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize,PowerNorm
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Patch,Rectangle,Polygon
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator,FuncFormatter
from pyproj import Geod
from shapely.geometry import box
from shapely.ops import polylabel
from vector_portable import read
import config

OUT=config.DIRS['out']/'11_integracao'/'apendices'

COLORS={'Atendimento':'#218649','Não atendimento':'#C43C39','Não classificado':'#e8e8e6','Informação insuficiente':'#e8e8e6',
 'Alta E / C não classificada':'#ba8755',
 'Alta E / Alta C':'#745779','Alta E / Baixa C':'#d6a277','Baixa E / Alta C':'#6b95b0','Baixa E / Baixa C':'#c2d7ce',
 'Ressuspensão viária urbana':'#d6b564','CSN – Casa de Pedra':'#8a719f','Vale – Fábrica':'#6f9f94','Vale – Viga':'#6b91b6',
 'Ferro+':'#c5837c','LGA Mineração':'#a3ac76','CSN – Namisa/Pires':'#ad8d65','Gerdau Ouro Branco':'#a6a0bc'}
COLORS.update({'Ressuspensão viária urbana':'#D8A447','CSN – Casa de Pedra':'#355C7D','Vale – Fábrica':'#408B82','Vale – Viga':'#769CC0','Ferro+':'#BC6655','LGA Mineração':'#8B9561','CSN – Namisa/Pires':'#937490','Gerdau Ouro Branco':'#5F6679'})
LABEL={'atendimento':'Atendimento','nao_atendimento':'Não atendimento','insuficiente':'Não classificado'}
COLORS.update({'Urbano Total':'#c5a85c','SCOF':'#956aa0','Ressuspensão urbana':'#d8a447'})
COLORS.update({'Alta E / Alta C':'#173f65','Alta E / Baixa C':'#f4cf70','Baixa E / Alta C':'#3798b3','Baixa E / Baixa C':'#bfe2b8'})

from groups import GROUPS
_group_colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f','#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#b15928','#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854']
COLORS.update({v['name']:c for v,c in zip(GROUPS.values(),_group_colors)})
COLORS.update({'CSN – Casa de Pedra':'#2b8cbe','Vale – Fábrica':'#41ab5d','Gerdau Ouro Branco':'#7fcdbb','Urbano Total':'#0b6580','Ferro+':'#c7e9b4','LGA Mineração':'#fdd49e','SCOF':'#c994c7','Todas as fontes':'#f2f2f2'})
COLORS.update({'Atendimento':'#83cdb6','Não atendimento':'#df4d50'})
GEO=Geod(ellps='GRS80')
_LABEL_CACHE={}

# Rounded scale ticks
def rounded_scale_ticks(norm):
    """Marcas legíveis nos valores reais, sem arredondar apenas os rótulos."""
    unit=10.**np.floor(np.log10(norm.vmax))
    norm.vmax=np.ceil(norm.vmax/unit)*unit
    raw=norm.inverse(np.linspace(0,1,4))
    ticks=[0.]
    for value in raw[1:-1]:
        step=10.**np.floor(np.log10(value))
        ticks.append(float(np.round(value/step)*step))
    return np.unique(ticks+[float(norm.vmax)])

# Centered legend
def centered_legend(fig,handles,ncol=3,*,y=.25,fontsize=9,row_step=.045,full_width=False,center=.535):
    """Bloco centralizado no encarte, com início fixo em cada coluna."""
    from matplotlib.font_manager import FontProperties
    renderer=fig.canvas.get_renderer();font=FontProperties(size=fontsize)
    em=fontsize*fig.dpi/72/fig.bbox.width
    widths=[max([max(renderer.get_text_width_height_descent(line,font,False)[0] for line in h.get_label().split('\n'))/fig.bbox.width+2.1*em for h in handles[c::ncol]] or [0]) for c in range(ncol)]
    gap=1.6*em;total=sum(widths)+gap*(ncol-1)
    left=center-total/2
    for row,start in enumerate(range(0,len(handles),ncol)):
        items=handles[start:start+ncol]
        short=len(items)<ncol
        rowwidth=sum(widths[:len(items)])+gap*(len(items)-1)
        x=center-rowwidth/2 if short else left
        for column,item in enumerate(items):
            anchor=.015+column*.97/ncol if full_width and not short else x+sum(widths[:column])+gap*column
            fig.legend(handles=[item],loc='upper left',bbox_to_anchor=(anchor,y-row*row_step),ncol=1,frameon=False,fontsize=fontsize,borderaxespad=0,handlelength=1.6,handletextpad=.5)

# Render
def render(z,muni,fields,code,titles,note,extent,*,stations=None,eligible=None,numeric=False,hatches=None,panel_layers=None,numeric_options=None,palette=None,surfaces=None,surface_legend=None,panel_shape=None,filename=None,figure_title=None,legend_categories=None,zone_layer=None,show_zones=True,station_overlay=None,atlas_scale=None,wind_directions=None,png_dpi=None):
    g=z.to_crs(4674);m=muni.to_crs(4674)
    import geopandas as gp
    ctx=gp.read_file(config.BASE/'base_regional'/'municipios_vizinhos_cache.geojson').to_crs(4674)
    ex=[extent[0]-.018,extent[1]-.025,extent[2]+.015,extent[3]+.026]
    clip=box(*ex);ctx=ctx[ctx.intersects(clip)].copy();ctx.geometry=ctx.geometry.intersection(clip)
    municipality_union=m.geometry.union_all()
    rows,cols=panel_shape or (1,len(fields))
    atlas=rows>1
    borders=(zone_layer if zone_layer is not None else z).to_crs(4674)
    zone_borders=borders.boundary if show_zones and borders.geom_type.isin(['Polygon','MultiPolygon']).all() else None
    fig,axes=plt.subplots(rows,cols,figsize=(8.27,11.69) if atlas else (7.4,5.35),squeeze=False)
    flat=axes.ravel()
    legend_rows=int(np.ceil(len(legend_categories or [])/3))
    atlas_bottom=.095+max(0,legend_rows-2)*.016
    fig.subplots_adjust(left=.045 if atlas else .085,right=.99 if atlas else .985,bottom=atlas_bottom if atlas else .26,top=.94 if atlas else .92,wspace=.035 if atlas else .10,hspace=.30 if atlas else .10)

    latref=np.mean([ex[1],ex[3]])
    _,_,ground_m=GEO.inv(ex[0],latref,ex[2],latref)
    for ax in flat:
        ax.set_xlim(ex[0],ex[2]);ax.set_ylim(ex[1],ex[3])
        ax.set_aspect(1/np.cos(np.deg2rad(latref)));ax.apply_aspect()
    paper_m=axes[0,0].get_position().width*fig.get_figwidth()*.0254
    denominator=int(atlas_scale) if atlas and atlas_scale is not None else int(round(ground_m/paper_m/5000)*5000) if atlas else 440000
    factor=ground_m/paper_m/denominator
    fig.set_size_inches(*(fig.get_size_inches()*factor))
    handles={}
    for j,(ax,field,title) in enumerate(zip(flat,fields,titles)):
        if panel_layers is not None:g=panel_layers[j].to_crs(4674)
        ctx.plot(ax=ax,color='#f7f6f2',edgecolor='#c0bdb5',linewidth=.45,zorder=0)
        for r in ctx.itertuples():
            if r.nome in ('Congonhas','Itaverava'):continue
            if r.geometry.area < .0006:continue
            cache_key=(r.nome,tuple(ex),r.geometry.wkb,municipality_union.wkb)
            if cache_key in _LABEL_CACHE:
                xx,yy,name=_LABEL_CACHE[cache_key]
                ax.text(xx,yy,name,ha='center',va='center',fontsize=5.7,color='#98948e',fontstyle='italic',clip_on=True,zorder=1)
                continue

            adjusted=r.nome in ('Moeda','São Brás do Suaçuí','Conselheiro Lafaiete','Itabirito')
            visible=r.geometry.intersection(box(ex[0]+.005,ex[1]+(.012 if adjusted else .04),ex[2]-.005,ex[3]-.006)).difference(m.geometry.union_all())
            if adjusted:
                for reserved in [box(ex[0],ex[1],ex[0]+.095,ex[1]+.038),box(ex[2]-.12,ex[1],ex[2],ex[1]+.052),box(ex[2]-.026,ex[3]-.045,ex[2],ex[3])]:
                    visible=visible.difference(reserved)
            parts=[v for v in getattr(visible,'geoms',[visible]) if v.geom_type=='Polygon' and not v.is_empty]
            if not parts:continue
            p=polylabel(max(parts,key=lambda v:v.area),tolerance=.0003)
            name=r.nome.replace('Conselheiro Lafaiete','Conselheiro\nLafaiete').replace('São Brás do Suaçuí','São Brás\ndo Suaçuí').replace('Ouro Branco','Ouro\nBranco').replace('Santana dos Montes','Santana dos\nMontes')
            xx,yy=p.x,p.y

            width=(.0042 if adjusted else .0046)*max(map(len,name.split('\n')))+.003
            height=(.009 if adjusted else .011)*len(name.split('\n'))+.003
            bx0,by0,bx1,by1=visible.bounds
            candidates=[]
            for cx in np.linspace(bx0+width/2,bx1-width/2,35):
                for cy in np.linspace(by0+height/2,by1-height/2,35):
                    label_box=box(cx-width/2,cy-height/2,cx+width/2,cy+height/2)
                    if visible.covers(label_box):candidates.append((cx,cy))
            if candidates:
                if adjusted:
                    xx,yy=max(candidates,key=lambda q:visible.boundary.distance(box(q[0]-width/2,q[1]-height/2,q[0]+width/2,q[1]+height/2)))
                else:xx,yy=min(candidates,key=lambda q:(q[0]-p.x)**2+(q[1]-p.y)**2)
            ax.text(xx,yy,name,ha='center',va='center',fontsize=5.7,color='#98948e',fontstyle='italic',clip_on=True,zorder=1)
            _LABEL_CACHE[cache_key]=(xx,yy,name)
        if stations is not None:
            g.plot(ax=ax,color='#eeeadf',edgecolor='none',linewidth=0)
            s=stations[j];b=s.copy();b.geometry=b.buffer(4000);b=b.to_crs(4674)
            ok=b.station_id.isin(eligible[j])
            for yes,color in [(False,'#d69e3b'),(True,'#2276ad')]:
                if (ok==yes).any():b.loc[ok==yes].plot(ax=ax,color=color,alpha=.40,edgecolor=color,linewidth=.60)
            for r in s.to_crs(4674).itertuples():
                ax.plot(r.geometry.x,r.geometry.y,'o',ms=2.4,color='#536c76')
                ax.annotate(str(r.number),(r.geometry.x,r.geometry.y),xytext=(3,3),textcoords='offset points',fontsize=6.8,fontweight='bold')
        elif surfaces is not None:
            from matplotlib.path import Path as PlotPath
            from matplotlib.patches import PathPatch
            import matplotlib.tri as mtri
            surface=surfaces[j]
            mesh=mtri.Triangulation(surface['x'],surface['y'])
            values=np.asarray(surface['values'])
            limits=surface['limits']
            from scipy.interpolate import CloughTocher2DInterpolator

            n=150 if atlas else 340
            gx=np.linspace(ex[0],ex[2],n);gy=np.linspace(ex[1],ex[3],n)
            xx,yy=np.meshgrid(gx,gy)
            values_grid=np.expm1(CloughTocher2DInterpolator(np.c_[surface['x'],surface['y']],np.log1p(values))(xx,yy))
            values_grid=np.ma.masked_invalid(np.clip(values_grid,0,float(values.max())))
            contours=ax.pcolormesh(xx,yy,values_grid,cmap=surface['cmap'],norm=surface['norm'],shading='gouraud',zorder=3,rasterized=True)
            vertices=[];commands=[]
            for polygon in getattr(municipality_union,'geoms',[municipality_union]):
                for ring in [polygon.exterior,*polygon.interiors]:
                    xy=np.asarray(ring.coords);vertices.extend(xy)
                    commands.extend([PlotPath.MOVETO]+[PlotPath.LINETO]*(len(xy)-2)+[PlotPath.CLOSEPOLY])
            contours.set_clip_path(PathPatch(PlotPath(vertices,commands),transform=ax.transData))
            surface['_bar_position']=ax.get_position().bounds
        elif numeric:
            if panel_layers is not None:
                (z.to_crs(4674) if show_zones else m).plot(ax=ax,facecolor='#d2dfcd' if show_zones else '#eeeadf',edgecolor='none',linewidth=0,zorder=1)
            v=g[field];good=v.notna()
            if (~good).any():g.loc[~good].plot(ax=ax,color='#e8e8e6',edgecolor='#b7b7b3',linewidth=.15)
            opts=numeric_options[j] if numeric_options else {}
            vmax=max(1,float(v.max())) if good.any() else 1.
            norm=opts.get('norm') or (PowerNorm(.5,vmin=0,vmax=vmax) if j==0 else Normalize(0,max(10,vmax)))
            rounded_ticks=rounded_scale_ticks(norm) if numeric_options and 'ticks' not in opts else None
            cmap=opts.get('cmap','YlGnBu' if j==0 else 'YlOrRd')
            if good.any():g.loc[good].plot(ax=ax,color=plt.get_cmap(cmap)(norm(v[good])),edgecolor='#9fa49e',linewidth=opts.get('linewidth',.15),markersize=opts.get('markersize',4))
            if opts.get('highlight_max') and good.any():
                peak=g.loc[v.eq(v.max())].geometry.representative_point()
                ax.scatter(peak.x,peak.y,s=18,facecolors='none',edgecolors='#182f36',linewidths=.7,zorder=8)
                handles['peak']=Line2D([],[],marker='o',ls='',mfc='none',mec='#182f36',ms=4,label='Maior valor no município')
            pos=ax.get_position();cax=fig.add_axes([pos.x0,.22,pos.width,.022])
            cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),cax=cax,orientation='horizontal')
            cb.ax.tick_params(labelsize=9,length=2);cb.set_label(opts.get('label','Habitantes estimados' if j==0 else 'Fração potencialmente\nevitável (%)'),fontsize=9)
            if not numeric_options:
                if j==0:cb.set_ticks([0,1000,3000,5000] if vmax>5000 else np.linspace(0,vmax,4))
                else:cb.set_ticks([0,2,4,6,8,10])
            else:
                ticks=opts.get('ticks')
                if ticks is None:ticks=rounded_ticks
                cb.set_ticks(ticks)
                cb.ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:,.0f}'.replace(',','.') if abs(v)>=100 else f'{v:.1f}'.rstrip('0').rstrip('.').replace('.',',')))
                if 'ticklabels' in opts:
                    cb.set_ticklabels(opts['ticklabels']);cb.ax.tick_params(labelsize=6.8)
                cb.ax.get_xticklabels()[0].set_horizontalalignment('left')
                cb.ax.get_xticklabels()[-1].set_horizontalalignment('right')
            if opts.get('show_missing',True):handles['missing']=Patch(facecolor='#e8e8e6',edgecolor='#aaa',label='Sem estimativa elegível')
        else:
            if panel_layers is not None and not show_zones:m.plot(ax=ax,facecolor='#eeeadf',edgecolor='none',zorder=1)
            if code=='G2':z.to_crs(4674).plot(ax=ax,facecolor='#e1eadc',edgecolor='none',linewidth=0,zorder=2)
            vals=g[field].fillna('Informação insuficiente').replace(LABEL)
            for cat in dict.fromkeys(vals):
                color=(palette or COLORS).get(cat,'#b3aaa0')
                road_width={'Rodovias principais':.45,'Vias secundárias':.30,'Vias locais e demais caminhos':.16}.get(cat,.40)
                g.loc[vals.eq(cat)].plot(ax=ax,color=color,edgecolor='none',linewidth=road_width if panel_layers is not None else 0,markersize=1.5 if code=='G2' else 5,alpha=.75 if code=='G2' else 1,zorder=3)
                handles[cat]=Patch(facecolor=color,edgecolor='#aaa',linewidth=.4,label=cat)

        if zone_borders is not None:

            zone_borders.plot(ax=ax,color='#405b64',linewidth=.18 if not atlas else .065,zorder=7)
        m.boundary.plot(ax=ax,color='#35413d',linewidth=1.05,zorder=8)
        if station_overlay is not None:
            overlay=station_overlay[j].to_crs(4674)
            ax.scatter(overlay.geometry.x,overlay.geometry.y,s=3 if atlas else 10,facecolor='white',edgecolor='#142e42',linewidth=.5,zorder=10)
        ax.set_xlim(ex[0],ex[2]);ax.set_ylim(ex[1],ex[3]);ax.set_aspect(1/np.cos(np.deg2rad(np.mean([ex[1],ex[3]]))))

        ax.set_xticks(np.arange(np.ceil(ex[0]/.10)*.10,ex[2],.10))
        yt=np.round(np.mean([ex[1],ex[3]])+np.array([-.08,0,.08]),2)
        ax.set_yticks(yt[(yt>ex[1]+.025)&(yt<ex[3]-.025)])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°O'.replace('.',',')))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°S'.replace('.',',')))
        ax.tick_params(labelsize=8.5,length=2,pad=3.5);ax.tick_params(axis='y',labelrotation=90,labelleft=j%cols==0)
        for label in ax.get_yticklabels():
            label.set_verticalalignment('center')
            label.set_horizontalalignment('center')
            label.set_rotation_mode('anchor')
        ax.tick_params(axis='y',pad=5.5)
        import textwrap
        title='\n'.join(textwrap.wrap(title,27)) if atlas else '\n'.join(textwrap.wrap(title,34 if cols>1 else 65))
        ax.set_xlabel('');ax.set_ylabel('');ax.set_title(title,fontsize=10.5,fontweight='bold',pad=4 if atlas else 4)
        ax.grid(alpha=.10,linewidth=.4)

        ax.set_axis_on()
        ax.set_frame_on(True)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#35413d')
            spine.set_linewidth(.55 if atlas else .65)

        ax.text(.965,.955,'N',transform=ax.transAxes,ha='center',va='bottom',fontsize=8,fontweight='bold',color='#39433f')
        ax.annotate('',xy=(.965,.946),xytext=(.965,.858),xycoords='axes fraction',
                    arrowprops=dict(arrowstyle='-|>',mutation_scale=5 if atlas else 14,lw=.55 if atlas else 1.2,color='#39433f',shrinkA=0,shrinkB=0),zorder=12)
        ax.apply_aspect()
        paper_m=ax.get_position().width*fig.get_figwidth()*.0254
        assert np.isclose(ground_m/paper_m,denominator,rtol=1e-8), 'Escala física incompatível'
        scale_text=f'{denominator:,}'.replace(',','.')
        if not atlas:ax.text(.97,.025,f'Datum: SIRGAS 2000\nGeográficas · EPSG:4674\nEscala 1:{scale_text}',transform=ax.transAxes,ha='right',va='bottom',multialignment='center',fontsize=5.7,color='#646962',linespacing=1.2,bbox=dict(boxstyle='round,pad=.35,rounding_size=.15',facecolor='white',edgecolor='#b9bdb6',linewidth=.45,alpha=.93),zorder=15)

        if atlas:continue
        x=ex[0]+.025;y=ex[1]+.020
        xmid,_,_=GEO.fwd(x,y,90,2500);xend,_,_=GEO.fwd(x,y,90,5000)
        h=(ex[3]-ex[1])*.012
        ax.add_patch(Rectangle((x,y),xmid-x,h,facecolor='#4b504c',edgecolor='#4b504c',lw=.5,zorder=10))
        ax.add_patch(Rectangle((xmid,y),xend-xmid,h,facecolor='white',edgecolor='#4b504c',lw=.5,zorder=10))
        for xx,lab in [(x,'0'),(xmid,'2,5'),(xend,'5 km')]:ax.text(xx,y-(ex[3]-ex[1])*.016,lab,ha='center',va='top',fontsize=6.3,zorder=11)
    if atlas:

        if cols==2:
            width=min(ax.get_position().width for ax in flat)
            gap=.045;left=.51-(2*width+gap)/2
            for j,ax in enumerate(flat):
                position=ax.get_position()
                ax.set_position([left+(j%cols)*(width+gap),position.y0,width,position.height])

        for ax in flat:
            for text in [*ax.texts,ax.title,*ax.get_xticklabels(),*ax.get_yticklabels()]:text.set_fontsize(text.get_fontsize()*.46)
            ax.title.set_fontsize(5.7)
            ax.tick_params(length=1,pad=2)
            for ann in ax.texts:
                if getattr(ann,'arrow_patch',None) is not None:
                    ann.arrow_patch.set_mutation_scale(4);ann.arrow_patch.set_linewidth(.4)
            for spine in ax.spines.values():spine.set_linewidth(.55)
    if stations is not None:
        handles={'a':Patch(facecolor='#2276ad',alpha=.55,label='Estação elegível no triênio'),'b':Patch(facecolor='#d69e3b',alpha=.55,label='Sem elegibilidade no triênio')}
    bottom=min(ax.get_position().y0 for ax in flat)
    if atlas:

            fig.text(.51,bottom-.020,f'Datum: SIRGAS 2000 · Geográficas (EPSG:4674)\nEscala 1:{denominator:,}'.replace(',','.'),ha='center',va='center',multialignment='center',fontsize=5.5,linespacing=1.2,bbox=dict(boxstyle='round,pad=.35,rounding_size=.15',facecolor='white',edgecolor='#b9bdb6',linewidth=.45))
            length=(20000/denominator)/(.0254*fig.get_figwidth())
            sx=.51-length/2;sy=bottom-.050
            for offset,color in [(0,'#35413d'),(length/2,'white')]:
                fig.add_artist(Rectangle((sx+offset,sy),length/2,.004,transform=fig.transFigure,facecolor=color,edgecolor='#35413d',lw=.4))
            for xx,lab in [(sx,'0'),(sx+length/2,'10'),(sx+length,'20 km')]:fig.text(xx,sy-.003,lab,ha='center',va='top',fontsize=5)
    if surfaces is not None:

        atlas_left=min(ax.get_position().x0 for ax in flat)
        atlas_width=max(ax.get_position().x1 for ax in flat)-atlas_left
        bar_specs=[(surfaces[0],atlas_left,bottom-.087,atlas_width)] if atlas else [(s,ax.get_position().x0,bottom-.078,ax.get_position().width) for s,ax in zip(surfaces,flat)]
        for s,x,y,w in bar_specs:
            cax=fig.add_axes([x,y,w,.012 if atlas else .022])
            cb=fig.colorbar(ScalarMappable(norm=s['norm'],cmap=s['cmap']),cax=cax,orientation='horizontal',extend='max',extendfrac=.04)
            cb.set_ticks(s['ticks'][:-1]);cb.ax.tick_params(labelsize=5 if atlas else 7.5,length=2)
            cb.ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:,.0f}'.replace(',','.') if v>=100 else f'{v:g}'.replace('.',',')))
            cb.set_label('Concentração (µg/m³)',fontsize=5.5 if atlas else 8)
            vmax=s.get('actual_max',float(np.max(s['values'])))
            maximum=f'{vmax:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
            if s.get('max_in_label'):
                cb.set_label(f'Concentração (µg/m³) · Máx. {maximum}',fontsize=7)
            else:cb.ax.text(1.035,-.85,f'Máx. {maximum}',transform=cb.ax.transAxes,ha='right',va='top',fontsize=5 if atlas else 7)
    elif code=='C1':

        has_missing=any(k in handles for k in ['Alta E / C não classificada','Informação insuficiente'])
        lax=fig.add_axes([.285 if has_missing else .47,.145,.13,.085]);lax.set_xlim(0,2);lax.set_ylim(0,2)
        for x in range(2):
            for y in range(2):lax.add_patch(Rectangle((x,y),1,1,facecolor=COLORS[('Alta E' if x else 'Baixa E')+' / '+('Alta C' if y else 'Baixa C')],edgecolor='white'))
        lax.set_xticks([.5,1.5],['Baixa','Alta'],fontsize=8.5);lax.set_yticks([.5,1.5],['Baixa','Alta'],fontsize=8.5)
        lax.set_xlabel('Emissão',fontsize=7,labelpad=2);lax.set_ylabel('Concentração',fontsize=7,labelpad=2)
        lax.tick_params(length=0);[s.set_visible(False) for s in lax.spines.values()]
        extra=[handles[k] for k in ['Alta E / C não classificada','Informação insuficiente'] if k in handles]
        fig.legend(handles=extra,loc='center',bbox_to_anchor=(.74,.19),frameon=False,fontsize=8)
    elif not numeric:
        if legend_categories is not None:
            handles={cat:Patch(facecolor=(palette or COLORS).get(cat,'#b3aaa0'),edgecolor='#aaa',linewidth=.3,label=cat) for cat in legend_categories}
        if code in ('B2','B3','B4','B5'):
            categories=('Atendimento','Não atendimento') if code in ('B4','B5') else ('Atendimento','Não atendimento','Não classificado')
            handles={cat:Patch(facecolor=COLORS[cat],edgecolor='#aaa',linewidth=.4,label=cat) for cat in categories}
        ncol=len(handles) if code.startswith('B') else 2 if code=='S1' else 3 if legend_categories is not None else 2
        if atlas:
            centered_legend(fig,list(handles.values()),ncol=3,y=bottom-.078,fontsize=5.8,row_step=.016,center=.51)
        elif code=='H2':
            centered_legend(fig,list(handles.values()),ncol=2,y=.205,fontsize=9,row_step=.045)
        else:
            centered_legend(fig,list(handles.values()),ncol=ncol,y=.205 if panel_layers is not None else .265,fontsize=9)
    else:fig.legend(handles=list(handles.values()),loc='center',bbox_to_anchor=(.535,.085),frameon=False,fontsize=8.5)
    if wind_directions is not None:
        from rosa_vento_seletor import add_to_figure
        assert len(set(wind_directions))==1, 'A figura pareada exige uma direção comum'
        base_height_pt=(fig.get_tightbbox(fig.canvas.get_renderer()).height+.09)*72
        rose_top=.07 if surfaces is not None else min(.07,.205-(max(1,int(np.ceil(len(handles)/ncol)))-1)*.045-.09)
        add_to_figure(fig,wind_directions[0],top=rose_top)
    if figure_title:fig.suptitle(figure_title,fontsize=11 if atlas else 12,fontweight='bold',y=.985)
    stem=filename or f'Figura_{code}'

    for ext in ['png','svg','pdf']:fig.savefig(OUT/f'{stem}.{ext}',dpi=png_dpi or (600 if atlas else 1000),facecolor='white',bbox_inches='tight',pad_inches=.045)
    if wind_directions is not None:
        svg_path=OUT/f'{stem}.svg';svg=svg_path.read_text(encoding='utf8')
        svg_path.write_text(svg.replace('<svg ',f'<svg data-base-height="{base_height_pt:.6f}" ',1),encoding='utf8')
    plt.close(fig)
