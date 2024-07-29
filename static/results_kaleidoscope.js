let symmetry = 7;
let angle = 360 / symmetry;
let table;
let currentRow = 0;

function preload() {
    // Load the CSV file from the static folder
    table = loadTable('static/data.csv', 'csv', 'header', () => {
        console.log('CSV Loaded successfully');
    }, (error) => {
        console.error('Error loading CSV:', error);
    });
}

function setup() {
    let canvas = createCanvas(720, 720);
    canvas.parent('canvas-container'); // Attach canvas to the div with id 'canvas-container'
    angleMode(DEGREES);
    background(255);
    colorMode(HSB, 360, 100, 100, 100);
    noiseDetail(25, 0.2);
    noLoop(); // Stop draw loop if not needed
}

function draw() {
    background(255); // Clear canvas
    translate(width / 2, height / 2);

    if (table) {
        if (currentRow < table.getRowCount()) {
            console.log('Drawing row:', currentRow); // Debug: Log the current row being processed

            let row = table.getRow(currentRow);
            let lineStartX = row.getNum('x1') - width / 2;
            let lineStartY = row.getNum('y1') - height / 2;
            let lineEndX = row.getNum('x2') - width / 2;
            let lineEndY = row.getNum('y2') - height / 2;
            let strokeW = row.getNum('width') * 2;
            let strokeColor = row.getNum('color') / 2;
            let saturation = row.getNum('+ or -');
            let brightness = row.getNum('+ or -');
            let alphaValue = row.getNum('+ or -') * 0.4;
            let noiseLevel = row.getNum('noise');

            console.log('Line coordinates:', lineStartX, lineStartY, lineEndX, lineEndY); // Debug: Log line coordinates
            console.log('Stroke settings:', strokeW, strokeColor, saturation, brightness, alphaValue); // Debug: Log stroke settings

            strokeWeight(strokeW);
            stroke(strokeColor, saturation, brightness, alphaValue);

            let segments = 2;
            for (let i = 0; i < symmetry; i++) {
                rotate(angle);
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

            currentRow++;
        } else {
            console.log('Finished drawing all rows');
        }
    } else {
        console.error('Table not loaded');
    }
}
