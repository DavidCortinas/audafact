const fs = require('fs');
const path = require('path');
const { createCanvas } = require('canvas');

// Define the path to assets directory
const assetsDir = path.join(__dirname, '../src/assets');

// Ensure assets directory exists
if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
}

const sizes = [16, 48, 128];

sizes.forEach(size => {
    const canvas = createCanvas(size, size);
    const ctx = canvas.getContext('2d');

    // Draw a simple placeholder icon
    ctx.fillStyle = '#4CAF50';
    ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = '#FFF';
    ctx.font = `${size/2}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('A', size/2, size/2);

    const buffer = canvas.toBuffer('image/png');
    const iconPath = path.join(assetsDir, `icon${size}.png`);
    
    fs.writeFileSync(iconPath, buffer);
    console.log(`Created icon: ${iconPath}`);
});

console.log('Icon generation complete!');
