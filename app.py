import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LAST CLASS", page_icon="🌘", layout="wide")
st.markdown("""
<style>
[data-testid="stApp"]{background:#08090d;color:#e8e9ed}
.block-container{max-width:1500px;padding-top:.7rem}
header{visibility:hidden}
</style>
""", unsafe_allow_html=True)
st.title("LAST CLASS")
st.caption("THE LAST NIGHT AT SCHOOL  |  3D SURVIVAL HORROR")
st.markdown("**WASD** 이동 · **마우스** 시점 · **E** 조사 · **Shift** 달리기 · **F** 손전등")
game = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;background:#030509;overflow:hidden;color:#eee;font-family:Arial}
#hud{position:absolute;z-index:2;top:16px;left:18px;font-size:13px;line-height:1.7;text-shadow:0 2px 8px #000}
#objective{position:absolute;right:18px;top:16px;z-index:2;text-align:right;font-size:13px;text-shadow:0 2px 8px #000}
#prompt{position:absolute;bottom:13%;left:0;width:100%;z-index:2;text-align:center;font-size:16px;text-shadow:0 2px 8px #000}
#cross{position:absolute;left:50%;top:50%;z-index:2;transform:translate(-50%,-50%);opacity:.65}
#veil{position:absolute;z-index:5;inset:0;background:radial-gradient(ellipse,#10141b 0%,#020306 85%);display:flex;align-items:center;justify-content:center;text-align:center}
#panel{max-width:680px;padding:28px 36px;border:1px solid #34343b;background:rgba(5,6,10,.92)}
h1{letter-spacing:9px;font-size:46px;margin:0 0 12px;color:#e8e8eb}button{background:#8f1725;color:#fff;border:0;padding:14px 28px;font-size:15px;letter-spacing:2px;cursor:pointer}
</style></head><body>
<div id="hud">LAST CLASS<br><span id="lamp">손전등: ON</span><br><span id="found">기록: 0 / 5</span></div>
<div id="objective">목표: 학교 기록 5개를 찾으세요</div><div id="cross">+</div><div id="prompt">주변을 조사하라.</div>
<div id="veil"><div id="panel"><h1>LAST CLASS</h1><p>학교에 남겨진 기록 5개를 찾아<br>잠긴 출구를 열어라.</p><p>WASD 이동 · 마우스 시점 · E 조사 · Shift 달리기 · F 손전등</p><button id="start">ENTER SCHOOL</button><p style="color:#777;font-size:12px;margin-top:20px">헤드폰과 어두운 환경에서 플레이하면 몰입감이 높아질 수 있습니다.</p></div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
<script>
(()=> {
const scene=new THREE.Scene();scene.background=new THREE.Color(0x030509);scene.fog=new THREE.FogExp2(0x030509,.045);
const camera=new THREE.PerspectiveCamera(76,innerWidth/innerHeight,.1,80);
camera.position.set(0,1.65,12);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;document.body.appendChild(renderer.domElement);
const ambient=new THREE.HemisphereLight(0x48536a,0x08080c,.38);scene.add(ambient);
const playerLight=new THREE.SpotLight(0xdde6ff,60,22,Math.PI/7,.45,1.5);playerLight.position.copy(camera.position);playerLight.target.position.set(0,0,-1);camera.add(playerLight);camera.add(playerLight.target);scene.add(camera);
const redLight=new THREE.PointLight(0x641020,1.2,8);redLight.position.set(0,2,-23);scene.add(redLight);
const M=(c,r=.8)=>new THREE.MeshStandardMaterial({color:c,roughness:r});
const wall=M(0x252a32), floor=M(0x292a2d), trim=M(0x393c42), desk=M(0x3a3027), black=M(0x08090b);
function mesh(g,m,x,y,z,cast=true){let o=new THREE.Mesh(g,m);o.position.set(x,y,z);o.castShadow=cast;o.receiveShadow=true;scene.add(o);return o}
function box(x,y,z,w,h,d,m){return mesh(new THREE.BoxGeometry(w,h,d),m,x,y,z)}
// corridor + adjoining room illusion, boundaries
box(0,-.12,0,38,.24,50,floor);box(0,3,-25,38,6,.35,wall);box(0,3,25,38,6,.35,wall);box(-19,3,0,.35,6,50,wall);box(19,3,0,.35,6,50,wall);
box(-7,3,0,.3,6,42,wall);box(7,3,0,.3,6,42,wall);
// hallway doors/ classroom windows
for(let z=-22;z<=20;z+=6){
 for(let side of [-1,1]){
  let x=side*7.02;
  box(x,1.45,z, .1,2.9,2.3,desk);
  box(x-side*.1,3.4,z, .12,1.15,2.5,trim);
 }
 box(0,5.9,z,2.3,.12,.3,trim);
}
// furniture rows and lockers
for(let z=-18;z<19;z+=4){
 for(let x of [-15,-12,12,15]){
  box(x,1.25,z,2.5,2.5,.25,trim);
  box(x,2.55,z,.2,.12,.35,desk);
 }
}
for(let z=-17;z<18;z+=5){
 for(let x of [-3.8,3.8]){
  box(x,.85,z,1.5,.12,1.1,desk);box(x,1.35,z-.25,1.3,.75,.1,desk);
 }
}
for(let x=-16;x<=16;x+=4){let lamp=box(x,5.85,0,1.8,.1,.5,trim);let light=new THREE.PointLight(0x8897b7,.35,9);light.position.set(x,5.2,0);scene.add(light);}
// room signs, environmental detail
function sign(text,x,z){let c=document.createElement('canvas');c.width=512;c.height=128;let ctx=c.getContext('2d');ctx.fillStyle='#10141b';ctx.fillRect(0,0,512,128);ctx.strokeStyle='#535963';ctx.strokeRect(4,4,504,120);ctx.fillStyle='#d5d8de';ctx.font='bold 40px sans-serif';ctx.textAlign='center';ctx.fillText(text,256,78);let t=new THREE.CanvasTexture(c);let o=mesh(new THREE.PlaneGeometry(3,0.75),new THREE.MeshBasicMaterial({map:t}),x,3.9,z,false);o.rotation.y=Math.PI;}
sign('3F  CLASSROOM',0,-21);sign('SCIENCE ROOM',-10,-5);sign('LIBRARY',10,7);
// notes/record markers with emissive glow
const notes=[
 {p:[-14,1,-16],t:'기록 01 — 야간 경비일지: 복도 끝에서 종소리가 들려도 확인하지 말 것.'},
 {p:[14,1,-8],t:'기록 02 — 학생들은 빈 교실의 창문에 누군가 서 있다고 말했다.'},
 {p:[-14,1,2],t:'기록 03 — 방송실은 폐쇄되었다. 그런데 매일 0시 방송이 송출된다.'},
 {p:[14,1,12],t:'기록 04 — 교무실 열쇠가 사라졌다. 분명 책상 서랍에 넣었는데.'},
 {p:[0,1,18],t:'기록 05 — 마지막 메모: 문이 열리면 뒤돌아보지 마.'}
];
let noteMeshes=[];let got=new Set();
notes.forEach((n,i)=>{let group=new THREE.Group();group.position.set(...n.p);scene.add(group);let paper=new THREE.Mesh(new THREE.BoxGeometry(.5,.07,.38),M(0xb9a981));group.add(paper);let glow=new THREE.PointLight(0x8b9ac0,.5,2.5);glow.position.y=.4;group.add(glow);group.userData.i=i;noteMeshes.push(group);});
const exitDoor=box(0,1.5,-24,3.2,3,.35,M(0x48171c));exitDoor.material.emissive=new THREE.Color(0x24070a);
const exitLabel=sign('EXIT',0,-23.4);
// creature design: stylized disturbing lanky shadow, avoid graphic gore
let monster=new THREE.Group();scene.add(monster);monster.visible=false;
const mskin=M(0x47434a), mcloth=M(0x0b0c10), faceMat=new THREE.MeshBasicMaterial({color:0x020203}), eye=new THREE.MeshBasicMaterial({color:0xa51d31});
function c(g,m,x,y,z){let o=new THREE.Mesh(g,m);o.position.set(x,y,z);o.castShadow=true;monster.add(o);return o}
c(new THREE.SphereGeometry(.42,18,16),mskin,0,2.6,0).scale.set(.68,1.18,.62);
c(new THREE.CylinderGeometry(.12,.2,1.65,10),mcloth,0,1.35,0);
let arm1=c(new THREE.CylinderGeometry(.06,.12,1.9,8),mcloth,-.58,1.4,0);arm1.rotation.z=.14;
let arm2=c(new THREE.CylinderGeometry(.06,.12,1.9,8),mcloth,.58,1.4,0);arm2.rotation.z=-.14;
let leg1=c(new THREE.CylinderGeometry(.07,.11,2.15,8),mcloth,-.2,-.35,0);
let leg2=c(new THREE.CylinderGeometry(.07,.11,2.15,8),mcloth,.2,-.35,0);
let mask=c(new THREE.SphereGeometry(.22,14,12),faceMat,0,2.58,.3);mask.scale.set(.9,1.15,.4);
c(new THREE.SphereGeometry(.045,8,8),eye,-.1,2.62,.48);c(new THREE.SphereGeometry(.045,8,8),eye,.1,2.62,.48);
let hair=c(new THREE.ConeGeometry(.4,1.3,9),mcloth,0,3.35,-.02);hair.rotation.x=.2;
// audio generated in-browser for ambient drone + heartbeat-ish pulse
let audio=null,osc=null,gain=null;
function audioStart(){try{audio=new (window.AudioContext||window.webkitAudioContext)();osc=audio.createOscillator();gain=audio.createGain();osc.type='sawtooth';osc.frequency.value=48;gain.gain.value=.025;osc.connect(gain);gain.connect(audio.destination);osc.start();}catch(e){}}
let state={started:false,yaw:0,pitch:0,keys:{},light:true,scare:0,monsterDelay:0};
const prompt=document.getElementById('prompt'),found=document.getElementById('found'),lamp=document.getElementById('lamp'),objective=document.getElementById('objective');
function start(){document.getElementById('veil').style.display='none';renderer.domElement.requestPointerLock();state.started=true;audioStart();}
document.getElementById('start').onclick=start;
document.addEventListener('pointerlockchange',()=>{});
document.addEventListener('mousemove',e=>{if(document.pointerLockElement===renderer.domElement){state.yaw-=e.movementX*.002;state.pitch-=e.movementY*.002;state.pitch=Math.max(-1.25,Math.min(1.25,state.pitch));camera.rotation.set(state.pitch,state.yaw,0,'YXZ');}});
document.addEventListener('keydown',e=>{state.keys[e.code]=true;if(e.code==='KeyE')interact();if(e.code==='KeyF'){state.light=!state.light;playerLight.visible=state.light;lamp.textContent='손전등: '+(state.light?'ON':'OFF');}});
document.addEventListener('keyup',e=>state.keys[e.code]=false);
renderer.domElement.addEventListener('click',()=>{if(state.started&&document.pointerLockElement!==renderer.domElement)renderer.domElement.requestPointerLock();});
function interact(){let nearest=null,dist=2.6;noteMeshes.forEach(o=>{if(got.has(o.userData.i))return;let d=camera.position.distanceTo(o.position);if(d<dist){dist=d;nearest=o;}});if(nearest){let i=nearest.userData.i;got.add(i);nearest.visible=false;found.textContent='기록: '+got.size+' / 5';prompt.textContent=notes[i].t;objective.textContent=got.size===5?'목표: 출구로 돌아가세요':'목표: 기록 '+(5-got.size)+'개 더 찾기';if(got.size===5)prompt.textContent='모든 기록을 찾았다. 출구로 돌아가라.';return;}if(camera.position.distanceTo(exitDoor.position)<3.8){if(got.size===5){end(true);}else prompt.textContent='출구가 잠겨 있다. 기록을 모두 찾아야 한다.';}}
function end(success){document.exitPointerLock?.();document.getElementById('veil').style.display='flex';document.getElementById('panel').innerHTML='<h1>'+(success?'ESCAPED':'')+'</h1><p>'+ (success?'학교를 빠져나왔다. 그런데 복도 끝에서 종소리가 다시 울렸다.':'')+'</p><button onclick="location.reload()">RESTART</button>';}
const clock=new THREE.Clock();
function update(){let dt=Math.min(clock.getDelta(),.04);if(state.started&&document.pointerLockElement===renderer.domElement){
let sp=state.keys.ShiftLeft?4.7:2.9;let v=new THREE.Vector3();if(state.keys.KeyW)v.z-=1;if(state.keys.KeyS)v.z+=1;if(state.keys.KeyA)v.x-=1;if(state.keys.KeyD)v.x+=1;v.normalize().applyAxisAngle(new THREE.Vector3(0,1,0),state.yaw);camera.position.addScaledVector(v,sp*dt);camera.position.x=Math.max(-18,Math.min(18,camera.position.x));camera.position.z=Math.max(-23,Math.min(23,camera.position.z));camera.position.y=1.65;
if(!monster.visible&&got.size>=1&&clock.elapsedTime>15){monster.visible=true;monster.position.set(0,0,-15);prompt.textContent='你听到了脚步声…';}
if(monster.visible){let delta=camera.position.clone().sub(monster.position);delta.y=0;let distance=delta.length();if(distance>2.7){delta.normalize();monster.position.addScaledVector(delta,dt*(got.size>=3?1.05:.38));}monster.lookAt(camera.position.x,0,camera.position.z);if(distance<5&&Math.random()<.008)prompt.textContent='복도에서 무언가 움직였다.';if(distance<1.6){prompt.textContent='시야가 흔들린다…';state.scare+=dt;if(state.scare>1.8){camera.position.z+=1.3;state.scare=0;}}}
if(audio&&gain){gain.gain.value=state.light?.018:.03;osc.frequency.value=state.light?45:58;}
}}
function loop(){requestAnimationFrame(loop);update();renderer.render(scene,camera);}loop();
window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
})();
</script></body></html>"""
components.html(game, height=760, scrolling=False)
st.markdown("### 플레이")
st.markdown("기록 5개를 찾은 뒤 출구로 돌아가세요. 3D 화면 내부를 클릭하면 마우스 시점 제어가 활성화됩니다.")
st.caption("브라우저에서 Three.js CDN을 불러오므로 배포 환경에서 인터넷 연결이 필요합니다.")
