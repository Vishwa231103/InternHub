import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, Stars } from "@react-three/drei";
import { useRef } from "react";


function FloatingCube({ position, size = 1 }) {
  const meshRef = useRef();

  useFrame((state, delta) => {
    if (!meshRef.current) return;

    meshRef.current.rotation.x += delta * 0.3;
    meshRef.current.rotation.y += delta * 0.5;
  });

  return (
    <Float
      speed={2}
      rotationIntensity={1}
      floatIntensity={2}
    >
      <mesh
        ref={meshRef}
        position={position}
        scale={size}
      >
        <boxGeometry args={[1, 1, 1]} />

        <meshStandardMaterial
          color="#00e5ff"
          wireframe
        />
      </mesh>
    </Float>
  );
}


function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />

      <pointLight
        position={[5, 5, 5]}
        intensity={2}
      />

      <Stars
        radius={50}
        depth={30}
        count={1500}
        factor={2}
        saturation={0}
        fade
        speed={1}
      />

      <FloatingCube
        position={[-4, 1, -2]}
        size={1.2}
      />

      <FloatingCube
        position={[4, -1, -3]}
        size={0.8}
      />

      <FloatingCube
        position={[3, 2, -5]}
        size={0.5}
      />

      <FloatingCube
        position={[-3, -2, -4]}
        size={0.7}
      />
    </>
  );
}


export default function ThreeBackground() {
  return (
    <div className="three-background">

      <Canvas
        camera={{
          position: [0, 0, 8],
          fov: 60,
        }}
      >

        <Scene />

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.3}
        />

      </Canvas>

    </div>
  );
}