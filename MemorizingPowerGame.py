import pygame
from scripts import game_config as gc
from pygame import display, event, image
from scripts import animal
from time import sleep
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

x=gc.INITIAL_POSITION_X
y=gc.INITIAL_POSITION_Y

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

def find_index(x, y):
    row=y//gc.IMAGE_SIZE
    col=x//gc.IMAGE_SIZE
    index=row*gc.NUM_TILES_SIDE+col
    return index

display.set_caption("Memorizing Power")
screen=display.set_mode((512, 580))
gameIcon = pygame.image.load("icon/icon.png")
pygame.display.set_icon(gameIcon)

matched=image.load('other_assets/matched.png')
button=image.load('other_assets/button.png')

running=True
tiles=[animal.Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]
current_images=[]
TOTAL_MOVES=0 

def exit(root):
    root.destroy()

while running:
    current_events=event.get()

    for e in current_events:

        if e.type==pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y=pygame.mouse.get_pos()
            if mouse_y<512:
                index=find_index(mouse_x, mouse_y)
                TOTAL_MOVES+=1
                if index not in current_images:
                    current_images.append(index)
                if len(current_images)>2:
                    current_images=current_images[1:]
            else:
                if mouse_x>=5 and mouse_x<=5+gc.BUTTON_WIDTH and mouse_y>=512 and mouse_y<=512+gc.BUTTON_HEIGHT:
                    root=Tk()
                    root.title("See Profile | Memorizing Power")
                    width=gc.PROFILE_WIDTH
                    height=gc.PROFILE_HEIGHT
                    screen_width=root.winfo_screenwidth()
                    screen_height=root.winfo_screenheight()
                    x_coordinate=80
                    y_coordinate=100
                    root.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))
                    root.minsize(width,height)
                    root.maxsize(width,height)
                    root.iconbitmap("icon/icon.ico")

                    conn=sqlite3.connect("database/records.db")
                    c=conn.cursor()

                    c.execute("SELECT *, 1 FROM record")
                    records=c.fetchall()

                    welcome="WELCOME"
                    welcomeLabel=Label(root, text=welcome, font=('Showcard Gothic', 30), fg="red")
                    welcomeLabel.pack(pady=(15,0))
                    if records[0][0]=='NO':
                        text1="Sorry!!! You have not fully completed the game!!!\nSo no data can be shown!!!\nPlease fully solve the puzzle first!!!\nBest Of Luck!!!"
                        label1=Label(root, text=text1, font=("Lucida Handwriting", 10), fg="green")
                        label1.pack(pady=(25,0))
                    else:
                        userScore=records[0][1]
                        text1="You have finished the puzzle in {} clicks!!!".format(userScore)
                        label1=Label(root, text=text1, font=("Lucida Handwriting", 10), fg="green")
                        label1.pack(pady=(25,0))

                    text2="You can solve the puzzle\nonly in 16 Mouse Clicks!!!"
                    label2=Label(root, text=text2, font=('Ravie', 15), fg="blue")
                    label2.pack(pady=(20,0))

                    okButton=Button(root, text="OK", font=('Showcard Gothic', 30), 
                        bg="#6ed28b", fg="#ae3bc6",
                        command=lambda:exit(root))
                    okButton.pack(pady=(20,0))

                    conn.commit()
                    conn.close()

                    root.mainloop()

        if e.type==pygame.QUIT:
            running=False

        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE:
                running=False

    screen.fill((255,255,255))

    total_skipped=0

    for _, tile in enumerate(tiles):
        image_i=tile.image if tile.index in current_images else tile.box
        if not tile.skip:
            screen.blit(image_i, (tile.col*gc.IMAGE_SIZE, tile.row*gc.IMAGE_SIZE))
        else:
            total_skipped+=1

    screen.blit(button, (5, 512))

    display.flip()

    if len(current_images)==2:
        idx1, idx2=current_images
        if tiles[idx1].name==tiles[idx2].name:
            tiles[idx1].skip=True
            tiles[idx2].skip=True
            sleep(0.4)
            screen.blit(matched, (0,0))
            display.flip()
            sleep(0.8)
            current_images=[]
            
    if total_skipped==len(tiles):
        conn=sqlite3.connect("database/records.db")
        c=conn.cursor()

        c.execute("SELECT *, 1 FROM record")
        records=c.fetchall()

        if records[0][0]=='NO':
            c.execute("""UPDATE record SET
            complete_minimum_one_time= :sayYes,   
            highest_score= :hS
            WHERE oid= :oid""",
            
            {
                'sayYes': 'YES',
                'hS':TOTAL_MOVES,

                'oid':str(1)
            }) 
        else:
            previous_hs=records[0][1]
            if previous_hs<TOTAL_MOVES:
                messagebox.showinfo("Bad Performance", "You take {} clicks to finish the puzzle!!!\nYou have done well in past!!! Don't be sad... You can do well!!!\nKEEP IT UP!!!".format(TOTAL_MOVES))
            elif previous_hs==TOTAL_MOVES:
                messagebox.showinfo("Great", "You take {} clicks to finish the puzzle!!!\nIt is same as your record!!!".format(TOTAL_MOVES))    
            else:
                messagebox.showinfo("Congratulations", "You take only {} clicks to finish the puzzle!!!\nIt is your new record!!!".format(TOTAL_MOVES))
                c.execute("""UPDATE record SET
                complete_minimum_one_time= :sayYes,   
                highest_score= :hS
                WHERE oid= :oid""",
                
                {
                    'sayYes': 'YES',
                    'hS':TOTAL_MOVES,

                    'oid':str(1)
                }) 
        conn.commit()
        conn.close()

        messagebox.showinfo("Good Bye", "Thanks for playing the game!!!\nSee you soon!!!")

        running=False

'''
#Execute for first time
conn=sqlite3.connect("database/records.db")
c=conn.cursor()

c.execute("""CREATE TABLE record(
            complete_minimum_one_time text,
            highest_score integer
            )""")

c.execute("INSERT INTO record VALUES (:complete_minimum_one_time, :highest_score)",
                    {
                    'complete_minimum_one_time':'NO',
                    'highest_score':0   
                    }
              )

conn.commit()
conn.close()
'''
pygame.quit()
