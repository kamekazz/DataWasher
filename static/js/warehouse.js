const container = document.getElementById('warehouse-container');
const spinner = document.getElementById('warehouse-spinner');
let scene, camera, renderer, forklift, controls, boxes = [];
let darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

function createForklift(THREE) {
    const group = new THREE.Group();
    const bodyGeo = new THREE.BoxGeometry(1, 0.5, 2);
    const bodyMat = new THREE.MeshStandardMaterial({color: 0xffaa00});
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.25;
    group.add(body);

    const mastGeo = new THREE.BoxGeometry(0.2, 1, 0.2);
    const mast = new THREE.Mesh(mastGeo, bodyMat);
    mast.position.set(0, 0.75, -0.8);
    group.add(mast);

    const forkGeo = new THREE.BoxGeometry(1, 0.05, 0.6);
    const fork = new THREE.Mesh(forkGeo, bodyMat);
    fork.position.set(0, 0.05, -1.1);
    group.add(fork);

    group.userData.velocity = 0;
    group.userData.rotationSpeed = 0;
    return group;
}

function handleTheme(THREE) {
    if (darkMode) {
        scene.background = new THREE.Color(0x111111);
        scene.fog = new THREE.Fog(0x111111, 10, 50);
    } else {
        scene.background = new THREE.Color(0xbfd1e5);
        scene.fog = new THREE.Fog(0xbfd1e5, 10, 50);
    }
}

async function init() {
    spinner.style.display = 'block';
    const [THREE, {OrbitControls}] = await Promise.all([
        import('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js'),
        import('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js')
    ]);

    scene = new THREE.Scene();
    handleTheme(THREE);
    camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
    camera.position.set(5,5,5);

    renderer = new THREE.WebGLRenderer({antialias:true});
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);

    const light = new THREE.HemisphereLight(0xffffff, darkMode?0x222222:0xffffff, 1);
    scene.add(light);
    const dir = new THREE.DirectionalLight(0xffffff, 0.5);
    dir.position.set(3,10,5);
    scene.add(dir);

    const res = await fetch('/static/maps/warehouse_map.json');
    const map = await res.json();

    const floorGeo = new THREE.PlaneGeometry(map.floor.width, map.floor.height);
    const floorMat = new THREE.MeshStandardMaterial({color: darkMode?0x444444:0xdddddd});
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI/2;
    scene.add(floor);

    map.racks.forEach(r => {
        const g = new THREE.BoxGeometry(r.width, r.height, r.depth);
        const m = new THREE.MeshStandardMaterial({color:0x808080});
        const rack = new THREE.Mesh(g,m);
        rack.position.set(r.x, r.height/2, r.z);
        rack.userData.isRack = true;
        scene.add(rack);
        boxes.push(new THREE.Box3().setFromObject(rack));
    });

    forklift = createForklift(THREE);
    scene.add(forklift);
    camera.lookAt(forklift.position);

    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth/container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    const keys = {};
    window.addEventListener('keydown', e => { keys[e.key.toLowerCase()] = true; });
    window.addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });

    function animate() {
        requestAnimationFrame(animate);
        const speed = 0.05;
        const turn = 0.03;
        if(keys['w'] || keys['arrowup']) forklift.userData.velocity = speed;
        else if(keys['s'] || keys['arrowdown']) forklift.userData.velocity = -speed;
        else forklift.userData.velocity = 0;
        if(keys['a'] || keys['arrowleft']) forklift.rotation.y += turn;
        if(keys['d'] || keys['arrowright']) forklift.rotation.y -= turn;
        if(forklift.userData.velocity !== 0) {
            const dir = new THREE.Vector3(0,0,-1).applyQuaternion(forklift.quaternion).multiplyScalar(forklift.userData.velocity);
            forklift.position.add(dir);
            const forkBox = new THREE.Box3().setFromObject(forklift);
            for(const box of boxes){
                if(forkBox.intersectsBox(box)){
                    forklift.position.sub(dir);
                    break;
                }
            }
        }
        renderer.render(scene, camera);
    }
    animate();
    spinner.style.display = 'none';

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        darkMode = e.matches;
        handleTheme(THREE);
    });

    window.addEventListener('beforeunload', () => {
        renderer.dispose();
    });
}

if(container){
    init();
}
