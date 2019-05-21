import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
Blue = (2,55,55)



def recursive_draw(x, y, width, height):
    """ Recursive rectangle function. """
    pygame.draw.rect(screen, WHITE,
                     [x, y, width, height],
                     1)
    speed = [10,0]
    rect_change_x = 10
    rect_change_y = 10




    # Is the rectangle wide enough to draw again?
    if (width > 25):
        # Scale down
        x += width * .1
        y += height * .1
        width *= .8
        height *= .8


               # Recursively draw again
        recursive_draw(x, y, width, height)

def recursive_draw2(x, y, width, height):
    """ Recursive rectangle function. """
    pygame.draw.rect(screen, Blue,
                     [x, y, width, height],
                     1)
    speed = [10,0]
    rect_change_x = 10
    rect_change_y = 10




    # Is the rectangle wide enough to draw again?
    if (width > 25):
        x += width * .1
        y += height * .1
        width *= .8
        height *= .8



               # Recursively draw again
        recursive_draw2(x, y, width, height)
def paused():
    screen.fill(black)

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)


        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)  


pygame.init()
#rectanglelist = [big()] 
# Set the height and width of the screen
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
black=(0,0,0)

end_it=False
time = 100

USEREVENT = 0

pygame.time.set_timer(USEREVENT+1, 10)
milliseconds = 0
seconds = 0
start_it = False
while (end_it==False):
    screen.fill(black)
    myfont=pygame.font.SysFont("Britannic Bold", 40)
    nlabel=myfont.render("Welcome to "+ " Jet shooter ", 1, (255, 0, 0))
    label=myfont.render("Click on the mouse to start ", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_it=True

    screen.blit(nlabel,(200, 100))
    screen.blit(label, (170,300))
    pygame.display.flip()

while (start_it==False):

    screen.fill(black)
    myfont2=pygame.font.SysFont("Britannic Bold", 40)
    label2=myfont2.render("Ready?", 1, (255, 0, 0))
    screen.blit(label2, (300,250))
    pygame.display.flip()
    pygame.time.wait(3000)
    start_it = True
fall = False   
while (fall==False):
    nlist = [3,2,1]
    for i in (nlist):


        screen.fill(black)
        n = str(i)
        myfont3=pygame.font.SysFont("Britannic Bold", 40)
        score = myfont3.render(n,1,(255,0,0))
        screen.blit((score), (350,250))
        pygame.display.flip()
        pygame.time.wait(1000)
    screen.fill(black)
    myfont4=pygame.font.SysFont("Britannic Bold", 40)
    label4=myfont3.render("GOOO!!!", 1, (255, 0, 0))
    screen.blit(label4, (300,250))
    pygame.display.flip()
    pygame.time.wait (1000)

    fall = True
pause = 0             
b = 0

# -------- Main Program Loop -----------
while not done:
        for event in pygame.event.get():

             if event.type == pygame.KEYUP:
                 if event.key==K_p:
                     pause=True
                 if pause == True:
                     screen.fill(black)
                     font=pygame.font.SysFont("Britannic Bold", 40)
                     nlabelBB=myfont.render("Pause", 1, (255, 0, 0))
                     screen.blit(nlabelBB,(200, 100))
                     pygame.display.flip()



        # Set the screen background
        screen.fill(BLACK)
        flip = 1
        a = 0

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT


        recursive_draw(0, 0, 700, 500)


        recursive_draw2(35,25, 625, 450)
###I TRIED TO PUT THE PAUSE GAME HERE AND IF PRESSED P PAUSE AND S CONTINUE
        while  a == 0 :


            if flip == 1 :
                recursive_draw(35,25,625,450)
                recursive_draw2(0, 0, 700, 500)

                flip = flip + 1
                pygame.display.flip()
                if event.type == pygame.KEYUP:
                     if event.key==K_p:
                         a = 1
                         screen.fill(black)
                         font=pygame.font.SysFont("Britannic Bold", 40)
                         nlabelBB=myfont.render("Pause", 1, (255, 0, 0))
                         screen.blit(nlabelBB,(200, 100))
                         pygame.display.flip()
                     if event.key==K_s:
                         a = 0





            if flip == 2 :
                recursive_draw(0, 0, 700, 500)
                recursive_draw2(35, 25, 625, 450)

                flip = flip - 1
                pygame.display.flip()
                if event.type == pygame.KEYUP:
                     if event.key==K_p:
                         a = 1
                         screen.fill(black)
                         font=pygame.font.SysFont("Britannic Bold", 40)
                         nlabelBB=myfont.render("Pause", 1, (255, 0, 0))
                         screen.blit(nlabelBB,(200, 100))
                         pygame.display.flip()
                     if event.key==K_s:
                         a = 0

        if event.type == pygame.QUIT:
            done = True





    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
pygame.display.flip()

    # Limit to 60 frames per second
clock.tick(20)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()