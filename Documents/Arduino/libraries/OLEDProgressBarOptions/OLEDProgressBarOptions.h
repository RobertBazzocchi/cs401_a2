void progressBar(void) {
  /* FUNCTION:
   *    Displays a progress bar that fills over 15 seconds to track hand washing progress
   */
  // define distance from side and bottom of the OLED screen
  int sideSpace = 5;
  int bottomSpace = 5;

  // define the x,y coordinates of the top left corner of rectangle and the rectangle's height and width
  int barHeight = 14;
  int barWidth = display.width()-2*sideSpace;
  int x = sideSpace;
  int y = display.height()-(bottomSpace+barHeight);

  // use the drawRect file to create an empty "progress bar"
  display.drawRect(x,y,barWidth,barHeight,WHITE);
  display.display();  
  int y0 = y+barHeight-1; // offset by 1 on OLED

  // fill the progress bar over 15 seconds
  for(int xbar=x; xbar < display.width()-sideSpace; xbar += 1){      
      display.drawLine(xbar,y0,xbar,y,WHITE);
      display.display();
      delay(80);
  }
  delay(2000);
//  display.clearDisplay();
}

void progressCircle(void) {
  /* FUNCTION:
   *    Displays a progress circle that fills over 15 seconds to track hand washing progress
   */
  int x0 = screenWidth/2;
  int y0 = screenHeight/2;
  int rBig = 32;
  int rSmall = 29;
  display.drawCircle(x0,y0,rBig,WHITE);
  display.drawCircle(x0,y0,rSmall-1,WHITE);
  display.display();
  
  // fill the progress bar over 15 seconds
  int xi;
  int yi;
  int xf;
  int yf;

  delay(2000);
  for(float theta=-pi/2; theta < 3*pi/2; theta += 0.015){ 
    xi = x0 + rSmall*cos(theta);
    yi = y0 + rSmall*sin(theta);
    xf = x0 + rBig*cos(theta);
    yf = y0 + rBig*sin(theta);
    display.drawLine(xi,yi,xf,yf,WHITE);
    display.display();
  } 
}

void progressMiniCircles(void) {
  /* FUNCTION:
   *    Displays a progress circle that fills over 15 seconds to track hand washing progress
   */
   
  int x0 = screenWidth/2;
  int y0 = screenHeight/2;
  int r = 25;
  int r_mini = 5;
  int num_circles = 12;
  // fill the progress bar over 15 seconds
  int xi;
  int yi;
  for(float theta=0; theta < 2*pi; theta += 2*pi/num_circles){      
    xi = x0 + r*cos(theta);
    yi = y0 + r*sin(theta);
    display.drawCircle(xi,yi,r_mini,WHITE);
  }
  display.display();
  delay(1000);
  for(float theta=0; theta < 2*pi; theta += 2*pi/num_circles){      
    xi = x0 + r*cos(theta);
    yi = y0 + r*sin(theta);
    display.fillCircle(xi,yi,r_mini,WHITE);
    display.display();
    delay(1100);
  }
}

void progressGuage(void) {
  /* FUNCTION:
   *    Displays a progress guage that fills over 15 seconds to track hand washing progress
   */
  // define distance from side and bottom of the OLED screen
  int sideSpace = 8;
  int bottomSpace = 5;

  int x0 = screenWidth/2;
  int y0 = screenHeight - bottomSpace;
  int r = 55;
  int r_small = 20;
  int r_mini = 10;

  // draw base of gauge
  display.drawLine(sideSpace,y0,screenWidth-sideSpace,y0,WHITE);
  display.drawLine(sideSpace-1,y0-3,sideSpace-1,y0+3,WHITE); // offset by one on OLED
  display.drawLine(screenWidth-sideSpace,y0-3,screenWidth-sideSpace,y0+3,WHITE);
  display.drawLine(x0,y0,x0,y0-r_mini,WHITE);
  display.display();
  
  delay(1000);
  // fill the progress bar over 15 seconds
  int xi;
  int yi;
  float dtheta = pi/14;
  int count = 15;
  int cursorX = 53;
  int cursorY = 30;
  display.setCursor(cursorX,cursorY);
  display.setTextColor(WHITE);        
  display.setTextSize(2);     
  display.println(count);
  display.display();
  delay(600);        
  display.fillRect(cursorX-10,cursorY-10,45,30,BLACK);     
  display.display();
  for(float theta=dtheta; theta < pi-dtheta; theta += dtheta){      
    xi = x0 - r*cos(theta);
    yi = y0 - r*sin(theta);
    
    if (count <= 10){
      cursorX = 60;
    }
    else{
      cursorX = 53;
    }
    display.setCursor(cursorX,cursorY);
    count -= 1;
    display.println(count);
    display.fillCircle(xi,yi,3,WHITE);
    display.display();
    delay(600);
    display.fillRect(cursorX-10,cursorY-10,45,45,BLACK);     
    display.drawLine(x0,y0,x0,y0-r_mini,WHITE);
    display.drawLine(sideSpace,y0,screenWidth-sideSpace,y0,WHITE);
    display.drawLine(sideSpace-1,y0-3,sideSpace-1,y0+3,WHITE); // offset by one on OLED
    display.drawLine(screenWidth-sideSpace,y0-3,screenWidth-sideSpace,y0+3,WHITE);
    display.display();
  }
  count-=1;
  display.setCursor(cursorX,cursorY);
  display.println(count);
  display.display();
  delay(1000);
}
