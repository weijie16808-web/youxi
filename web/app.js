import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const canvas=document.querySelector('#scene');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.shadowMap.enabled=true;
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(32,1,.1,2000); camera.position.set(225,180,270);
const controls=new OrbitControls(camera,canvas); controls.target.set(0,0,0); controls.enableDamping=true; controls.minDistance=160; controls.maxDistance=500;
scene.add(new THREE.HemisphereLight(0xffffff,0x28303b,3)); const key=new THREE.DirectionalLight(0xffffff,4);key.position.set(-180,260,200);key.castShadow=true;scene.add(key);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(1000,1000),new THREE.ShadowMaterial({color:0x56616d,opacity:.16}));floor.rotation.x=-Math.PI/2;floor.position.y=-45;floor.receiveShadow=true;scene.add(floor);
const g=new THREE.Group();scene.add(g); const dark=new THREE.MeshStandardMaterial({color:0x34363a,metalness:.75,roughness:.26});const edge=new THREE.MeshStandardMaterial({color:0x17191b,metalness:.5,roughness:.34});const black=new THREE.MeshStandardMaterial({color:0x06080c,metalness:.35,roughness:.18});const blue=new THREE.MeshPhysicalMaterial({color:0x135de8,metalness:.12,roughness:.08,clearcoat:1,emissive:0x07163a});
function mesh(geo,mat,pos,rot){const o=new THREE.Mesh(geo,mat);o.position.copy(pos||new THREE.Vector3);if(rot)o.rotation.set(...rot);o.castShadow=o.receiveShadow=true;g.add(o);return o}
function box(w,h,d,r,mat,pos){return mesh(new THREE.RoundedBoxGeometry(w,h,d,r,5),mat,pos)}
// dimensional coordinate: X=width 214, Y=height 82, Z=depth 168; camera looks at front (-Z)
box(214,82,168,8,dark,new THREE.Vector3(0,3,0)); box(207,5,161,3,edge,new THREE.Vector3(0,-40,0));
// feet
for(const x of [-84,84])for(const z of [-62,62])mesh(new THREE.CylinderGeometry(7,8,6,20),black,new THREE.Vector3(x,-44,z));
// front lens and sensor
mesh(new THREE.CylinderGeometry(29,29,4,48),edge,new THREE.Vector3(-47,5,-86),[Math.PI/2,0,0]);mesh(new THREE.CylinderGeometry(24,24,5,48),black,new THREE.Vector3(-47,5,-89),[Math.PI/2,0,0]);mesh(new THREE.CylinderGeometry(18,18,6,48),blue,new THREE.Vector3(-47,5,-92),[Math.PI/2,0,0]);box(20,12,3,5,black,new THREE.Vector3(57,4,-86));
// side ventilation grids
function vents(x,side){for(let row=0;row<8;row++)for(let col=0;col<16;col++){const z=-53+col*7;const y=-16+row*6;box(4,3,2,1,black,new THREE.Vector3(x,y,z));}}
vents(108);vents(-108);
// rear I/O panel and connectors
box(166,35,3,7,black,new THREE.Vector3(0,12,86));
for(const [x,w,label] of [[-65,22,''],[-33,19,''],[-5,19,'']])box(w,10,3,1,edge,new THREE.Vector3(x,15,89));
for(const x of [25,49,75])mesh(new THREE.CylinderGeometry(5,5,3,20),edge,new THREE.Vector3(x,15,89),[Math.PI/2,0,0]);
// top control marks
for(const x of [-26,-9,9,26])mesh(new THREE.CylinderGeometry(4,4,1,18),edge,new THREE.Vector3(x,45,15));
const targets={front:[0,22,310],rear:[0,25,-310],right:[310,15,0],top:[0,350,0],hero:[225,180,270]};
function view(name){const p=targets[name];controls.target.set(0,0,0);camera.position.set(...p);controls.update();document.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b.dataset.view===name));}
document.querySelectorAll('button').forEach(b=>b.onclick=()=>view(b.dataset.view));
function resize(){const r=canvas.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix()}addEventListener('resize',resize);resize();
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera)});
