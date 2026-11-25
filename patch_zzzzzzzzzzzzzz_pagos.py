# Pago con tarjeta (Redsys, TPV virtual del Banco Santander). Desde el 25/11/2026.
# 1) En las paginas con carrito: opcion "Pagar ahora con tarjeta" en los pedidos para recoger.
# 2) En las paginas con reservas: senal online para grupos (a partir de las personas que diga el Worker).
# 3) Crea /pago/ (pagina de vuelta del banco), que confirma el pago y muestra el resultado.
# Solo se activa si el Worker responde /api/pago/config. Mientras el Worker este en modo "pruebas",
# solo lo ve quien entra con ?pruebapago=1, asi los clientes no ven nada hasta pasar a modo "real".
# Va despues de los demas parches. Nunca rompe la publicacion.
import os, re, sys

MARCA = 'id="lc-pagos"'

JS = r'''<script id="lc-pagos">
(function(){
  if(typeof API==="undefined"||!API)return;
  var qs=new URLSearchParams(location.search);
  try{if(qs.get("pruebapago")==="1")sessionStorage.setItem("lc-pruebapago","1");if(qs.get("pruebapago")==="0")sessionStorage.removeItem("lc-pruebapago")}catch(e){}
  var prueba=false;try{prueba=sessionStorage.getItem("lc-pruebapago")==="1"}catch(e){}
  var P={on:false,modo:"",senal:{desde_pax:0,eur_persona:0},tarjeta:true};
  function eur(n){return n.toFixed(2).replace(".",",")+" €"}
  function irAlBanco(j){var f=document.createElement("form");f.method="POST";f.action=j.url;Object.keys(j.campos).forEach(function(k){var i=document.createElement("input");i.type="hidden";i.name=k;i.value=j.campos[k];f.appendChild(i)});document.body.appendChild(f);f.submit()}
  fetch(API+"/pago/config").then(function(r){return r.json()}).then(function(c){
    if(!c||!c.ok||!c.activo)return;
    if(c.modo!=="real"&&!prueba)return;
    P.on=true;P.modo=c.modo;P.senal=c.senal||P.senal;
    var dr=document.getElementById("drawer");
    if(typeof renderDrawer==="function"&&dr&&!dr.hidden)renderDrawer();
    senalUI();
  }).catch(function(){});

  /* ---- pedidos para recoger ---- */
  if(typeof placeOrder==="function"&&typeof renderDrawer==="function"){
    var origRender=renderDrawer,origPlace=placeOrder;
    window.renderDrawer=function(){
      origRender.apply(this,arguments);
      try{
        if(!P.on||dTab!=="cart"||order.step!=="checkout"||order.mode!=="pickup")return;
        var btn=document.getElementById("placeOrder");if(!btn||document.getElementById("paySel"))return;
        var d=document.createElement("div");d.id="paySel";d.className="paysel";
        d.innerHTML='<label><input type="radio" name="lcpay" value="tarjeta"'+(P.tarjeta?" checked":"")+'> <b>Pagar ahora con tarjeta</b> <span>(pago seguro Redsys · Banco Santander)</span></label>'+
          '<label><input type="radio" name="lcpay" value="tienda"'+(P.tarjeta?"":" checked")+'> Pagar al recoger</label>'+(P.modo!=="real"?'<p class="note" style="color:#a8402c">Modo pruebas: no se cobra dinero real.</p>':"");
        btn.parentNode.insertBefore(d,btn);
        var txt=function(){btn.textContent=P.tarjeta?"Pagar con tarjeta":"Preparar pedido"};txt();
        d.addEventListener("change",function(e){P.tarjeta=e.target.value==="tarjeta";txt()});
      }catch(e){}
    };
    window.placeOrder=async function(){
      if(!(P.on&&P.tarjeta&&order.mode==="pickup"))return origPlace.apply(this,arguments);
      var v=function(id){var el=document.querySelector(id);return(el&&el.value||"").trim()};
      Object.assign(order,{date:v("#oDate"),time:v("#oTime"),name:v("#oName"),phone:v("#oPhone"),notes:v("#oNotes")});
      var e=[];if(!order.name)e.push("tu nombre");if(order.phone.replace(/\D/g,"").length<9)e.push("un teléfono válido");if(!order.time)e.push("una hora de recogida");var ok=document.getElementById("oOk");if(ok&&!ok.checked)e.push("aceptar la política de privacidad");
      var err=document.getElementById("oErr");
      if(e.length){err.textContent="Falta "+e.join(", ")+".";err.hidden=false;return}
      var btn=document.getElementById("placeOrder");btn.disabled=true;btn.textContent="Conectando con el banco…";
      var j;try{j=await api("/pago/pedido",{items:cart,nombre:order.name,telefono:order.phone,fecha:order.date,hora:order.time,notas:order.notes,consentimiento:true,hp:v("#oHp")})}catch(x){j={ok:false,error:"No hemos podido conectar. Inténtalo de nuevo o elige pagar al recoger."}}
      if(!j||!j.ok){btn.disabled=false;btn.textContent="Pagar con tarjeta";err.textContent=(j&&j.error)||"No se ha podido iniciar el pago.";err.hidden=false;return}
      try{hist.push({kind:"order",ref:j.ref,when:"Recogida "+order.date+" a las "+order.time+" · pago con tarjeta",summary:cartLines().map(function(l){return l.q+"× "+l.m.t}).join(", "),total:j.importe/100,items:Object.assign({},cart),link:"/pago/?o="+j.pedido+"&r="+encodeURIComponent(j.ref),ts:Date.now()});hist=hist.slice(-30);save("lc-hist",hist)}catch(x){}
      irAlBanco(j);
    };
  }

  /* ---- senal de reserva para grupos ---- */
  function necesitaSenal(){return typeof RS!=="undefined"&&P.on&&P.senal.desde_pax>0&&!RS.demo&&!RS.espera&&RS.pax>=P.senal.desde_pax}
  function senalUI(){
    var b=document.getElementById("rSubmit");if(!b)return;
    var n=document.getElementById("senalNote");
    if(!n){n=document.createElement("p");n.id="senalNote";n.className="note";n.hidden=true;b.parentNode.insertBefore(n,b)}
    if(necesitaSenal()){
      var imp=P.senal.eur_persona*RS.pax;
      n.innerHTML="Para grupos de "+P.senal.desde_pax+" o más personas pedimos una <b>señal de "+eur(P.senal.eur_persona)+" por persona ("+eur(imp)+")</b>, que se descuenta de la cuenta. Se paga con tarjeta en la página segura del banco."+(P.modo!=="real"?' <span style="color:#a8402c">Modo pruebas: no se cobra dinero real.</span>':"");
      n.hidden=false;b.textContent="Pagar señal y reservar ("+eur(imp)+")";
    }else{n.hidden=true}
  }
  document.addEventListener("click",function(e){if(e.target.closest&&e.target.closest("#rBook"))setTimeout(senalUI,0)});
  document.addEventListener("submit",async function(ev){
    if(!ev.target||ev.target.id!=="resForm"||!necesitaSenal())return;
    ev.preventDefault();ev.stopImmediatePropagation();
    var v=function(id){return document.querySelector(id).value.trim()};var e=[];
    if(!RS.hora)e.push("una hora");if(!v("#rName"))e.push("tu nombre");if(v("#rPhone").replace(/\D/g,"").length<9)e.push("un teléfono válido");if(v("#rMail")&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v("#rMail")))e.push("un email válido");if(!document.getElementById("rOk").checked)e.push("aceptar la política de privacidad");
    var err=document.getElementById("rErr");
    if(e.length){err.textContent="Falta "+e.join(", ")+".";err.hidden=false;return}
    err.hidden=true;var b=document.getElementById("rSubmit");b.disabled=true;var prev=b.textContent;b.textContent="Conectando con el banco…";
    var body={fecha:RS.fecha,hora:RS.hora,pax:RS.pax,nombre:v("#rName"),telefono:v("#rPhone"),email:v("#rMail"),zona:v("#rZone"),notas:v("#rNotes"),consentimiento:true,espera:false,hp:v("#rHp")};
    var j;try{j=await api("/pago/senal",body)}catch(x){j={ok:false,error:"No hemos podido conectar. Inténtalo de nuevo o llámanos al "+PHONE+"."}}
    if(!j||!j.ok){b.disabled=false;b.textContent=prev;err.textContent=(j&&j.error)||"No se ha podido reservar.";err.hidden=false;if(j&&j.completo&&typeof loadAvail==="function")loadAvail();return}
    try{hist.push({kind:"res",ref:j.ref,when:RS.fecha+" · "+RS.hora,summary:RS.pax+" personas · "+body.nombre+" · señal "+j.importe_txt,link:"/reserva.html?t="+j.token,ts:Date.now()});hist=hist.slice(-30);save("lc-hist",hist)}catch(x){}
    irAlBanco(j);
  },true);
})();
</script>'''

CSS = ('<style id="lc-pagos-css">.paysel{display:grid;gap:6px;margin:0 0 10px;padding:10px 12px;border:1px solid rgba(0,0,0,.12);border-radius:10px;font-size:14px}'
       '.paysel label{display:flex;gap:8px;align-items:baseline;cursor:pointer}.paysel span{color:#6b6f78;font-size:12.5px}</style>')

PAGINA = r'''<main><h1 id="pt">Comprobando el pago…</h1><div id="pc"><p>Un momento, estamos confirmando el pago con el banco.</p></div>
<p style="margin-top:28px"><a href="/">← Volver a la web</a> · <a href="tel:+34919414881">919 41 48 81</a></p></main>
<script src="/config.js"></script>
<script>
(async function(){
  var API=(window.LC_API||"/api").replace(/\/$/,""),q=new URLSearchParams(location.search),o=q.get("o")||"",r=q.get("r")||"";
  var t=document.getElementById("pt"),c=document.getElementById("pc");
  function esc(s){return String(s).replace(/[&<>"]/g,function(x){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]})}
  if(q.get("Ds_MerchantParameters")&&q.get("Ds_Signature")){
    try{await fetch(API+"/pago/confirmar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({Ds_SignatureVersion:q.get("Ds_SignatureVersion"),Ds_MerchantParameters:q.get("Ds_MerchantParameters"),Ds_Signature:q.get("Ds_Signature")})})}catch(e){}
  }
  var j=null;
  for(var i=0;i<8;i++){
    try{j=await (await fetch(API+"/pago/estado?o="+encodeURIComponent(o)+"&r="+encodeURIComponent(r))).json()}catch(e){j=null}
    if(j&&j.ok&&j.estado!=="pendiente")break;
    if(q.get("ko"))break;
    await new Promise(function(f){setTimeout(f,2000)});
  }
  var prueba=j&&j.modo!=="real"?'<p class="ph">Modo pruebas: no se ha cobrado dinero real.</p>':"";
  if(j&&j.ok&&j.estado==="pagado"){
    if(j.tipo==="pedido"){
      try{localStorage.setItem("lc-cart","{}")}catch(e){}
      t.textContent="¡Pago recibido! Pedido "+j.ref;
      c.innerHTML="<p>Hemos recibido el pago de <b>"+esc(j.importe_txt)+"</b> y tu pedido ya está en cocina. Recógelo en C. de Ventura Rodríguez, 5 (Plaza de los Cubos) a la hora elegida.</p>"+(j.texto?"<pre style=\"white-space:pre-wrap;background:#fff;padding:12px;border-radius:8px\">"+esc(j.texto)+"</pre>":"")+prueba;
    }else{
      t.textContent="¡Reserva confirmada! "+j.ref;
      c.innerHTML="<p>Hemos recibido la señal de <b>"+esc(j.importe_txt)+"</b>, que se descontará de la cuenta. ¡Os esperamos!</p>"+(j.token?'<p><a href="/reserva.html?t='+encodeURIComponent(j.token)+'">Ver mi reserva</a></p>':"")+prueba;
    }
  }else if(j&&j.ok&&j.estado==="pendiente"&&!q.get("ko")){
    t.textContent="Pago en comprobación";
    c.innerHTML="<p>El banco todavía no nos ha confirmado el pago. Si te han cobrado, no te preocupes: en unos minutos quedará registrado. Ante cualquier duda llámanos al <b>919 41 48 81</b> y di la referencia <b>"+esc(r)+"</b>.</p>";
  }else{
    t.textContent="El pago no se ha completado";
    c.innerHTML="<p>No se ha realizado ningún cobro"+(j&&j.tipo==="senal"?" y la reserva no ha quedado guardada":"")+". Puedes volver a intentarlo"+(j&&j.tipo==="pedido"?" o elegir «Pagar al recoger»":"")+".</p><p><a href=\""+(j&&j.tipo==="senal"?"/reservas/":"/carta/")+"\">Volver a intentarlo</a></p>";
  }
})();
</script>'''


def pagina_pago(site):
    src = os.path.join(site, '404.html')
    dst = os.path.join(site, 'pago', 'index.html')
    if not os.path.isfile(src) or os.path.isfile(dst):
        return 0
    t = open(src, encoding='utf-8').read()
    if t.count('<main') != 1 or t.count('</main>') != 1:
        return 0
    t = re.sub(r'<title>.*?</title>', '<title>Pago · Lang City</title><meta name="robots" content="noindex">', t, count=1, flags=re.S)
    t = t[:t.find('<main')] + PAGINA + t[t.find('</main>') + len('</main>'):]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    return 1


def main(args):
    done = 0
    for a in args:
        if os.path.isdir(a):
            done += pagina_pago(a)
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            q = p.replace('\\', '/')
            if '/admin/' in q or '/pago/' in q:
                continue
            try:
                t = open(p, encoding='utf-8').read()
            except Exception:
                continue
            if MARCA in t or '</body>' not in t:
                continue
            if 'async function placeOrder' not in t and 'id="resForm"' not in t:
                continue
            n = t.replace('</head>', CSS + '</head>', 1)
            i = n.rfind('</body>')
            n = n[:i] + JS + n[i:]
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(n)
            done += 1
    print('pagos: %d archivos' % done)


if __name__ == '__main__':
    try:
        main(sys.argv[1:] or ['.'])
    except Exception as e:  # nunca rompe la publicacion
        print('pagos: error', e)
