import React from "react";

export default function CustomBrainIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <img
      src="/image.png"   // <-- stored in /public/image.png
      alt="Brain Icon"
      style={{
        width: props.width || 24,
        height: props.height || 24,
      }}
    />
  );
}
