// Wellbeing results kaleidoscope p5.js
// https://editor.p5js.org/amendajt/sketches/RQqCHN8dt

// to embed: <iframe src="https://editor.p5js.org/amendajt/full/RQqCHN8dt"></iframe>

// CODE:

let symmetry = 7;
let angle = 360 / symmetry;
let table; // Variable to store the loaded table
let currentRow = 0; // Keep track of the current row in the CSV

function preload() {
  // Load the CSV file
  table = loadTable('transformed_file.csv', 'csv', 'header');
}

function setup() {
  describe(
    `Dark grey canvas that reflects the lines drawn within it in ${symmetry} sections.`
  );
  createCanvas(720, 720);
  angleMode(DEGREES);
  background(255);
  colorMode(HSB, 360, 100, 100, 100); // Set HSB mode with hue, saturation, brightness, and alpha ranges
  noiseDetail(25, 0.2); // Adjust the noise function for more detail
}

function draw() {
  translate(width / 2, height / 2);

  if (currentRow < table.getRowCount()) {
    // Get the current row's data
    let row = table.getRow(currentRow);
    let lineStartX = row.getNum('x1') - width / 2;
    let lineStartY = row.getNum('y1') - height / 2;
    let lineEndX = row.getNum('x2') - width / 2;
    let lineEndY = row.getNum('y2') - height / 2;
    let strokeW = row.getNum('width') * 2;
    let strokeColor = row.getNum('color') / 2;
    let saturation = row.getNum('+ or -');
    let brightness = row.getNum('+ or -');
    let alphaValue = row.getNum('+ or -') * .4;
    let noiseLevel = row.getNum('noise'); // Get noise level from the CSV

    // Set stroke weight and color with opacity
    strokeWeight(strokeW * 2);
    stroke(strokeColor, saturation, brightness, alphaValue); // HSB mode with full saturation and brightness, and custom opacity

    // Number of segments to divide the line into
    let segments = 7;

    // Draw the lines for each symmetry section
    for (let i = 0; i < symmetry; i++) {
      rotate(angle);
      
      // Draw line segments with noise
      for (let j = 0; j < segments; j++) {
        let t1 = j / segments;
        let t2 = (j + 1) / segments;
        
        let x1 = lerp(lineStartX, lineEndX, t1) + noise(t1 * noiseLevel * 100) * 10;
        let y1 = lerp(lineStartY, lineEndY, t1) + noise(t1 * noiseLevel * 100) * 10;
        let x2 = lerp(lineStartX, lineEndX, t2) + noise(t2 * noiseLevel * 100) * 10;
        let y2 = lerp(lineStartY, lineEndY, t2) + noise(t2 * noiseLevel * 100) * 10;

        line(x1, y1, x2, y2);

        push();
        scale(1, -1);
        line(x1, y1, x2, y2);
        pop();
      }
    }

    // Move to the next row
    currentRow++;
  }
}
