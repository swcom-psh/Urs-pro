from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

__ = False

class Player(FirstPersonController):
     def __init__(self):
          super().__init__(
               speed = 10,
               model = 'cube',
               collider = 'box',
               scale = 1,
               gravity = 0.5,
               jump_height = 10
          )

class Exit(Entity):
     def __init__(self, x, z): # for문에서 전달한 i, j값을 Exit 클래스의 x, z 변수안에 저장
          super().__init__(
               model = 'cube',
               color = color.black90,
               position = (x * 5, 0, z * 5) , # 전달받은 i, j 값을 이용하여 좌표를 설정
               scale = (5, 5, 5)
          )
          self.clear = Text( #텍스트 객체를 생성하고, self.clear 변수에 저장합니다.
               text = '탈출성공', #출력할 메시지를 작성합니다.
               font = 'assets/강원교육튼튼.ttf', #폰트를 불러옵니다.
               scale = 2, #텍스트의 크기
               origin = (0,0), #텍스트의 좌표(2차원)
               visible = False #텍스트는 우선 눈에 보이지 않게 하였습니다.
          )
          self.player = player # 외부 플레이어의 정보를 Exit 클래스의 self.player 변수 안에 저장합니다.
     
     def update(self):
          self.playerCollision()
     

     def playerCollision(self): #플레이어와 충돌을 감지하는 메서드 함수를 정의합니다.
        distance = (self.player.position - self.position).length()
        #print(distance) 
        if distance < 3: #만약 플레이어가 탈출구에 근접하면
             self.clear.visible = True # 탈출 성공 메시지가 보이도록 설정합니다.
             self.player.enabled = False #탈출 성공 메시지가 출력된 후 플레이어가 비활성화됩니다.

class Warp(Entity):
     def __init__(self, x, z):
          super().__init__( #Entity의 속성을 그대로 물려받아 초기화하기 위해 작성하는 구문
               warp = Entity(
                    model = 'cube',
                    texture = 'assets/WarpTexture.png', #이 부분은 작성하지 않고 추후에 따로 추가해도됩니다.
                    position = (x * 5, 0, z * 5),
                    scale = (5, 5, 5),
                    collider = 'box'
               )                          
          )

          self.player = player #클래스 외부의 player에 대한 정보를 받아옵니다.
          
     def update(self): #게임 진행 과정 속 playerCollision 함수를 실행하여 충돌을 확인합니다.
          print(player.position) #플레이어의 좌표를 출력하여 좌표를 확인할 수 있습니다.
          self.playerCollision()

     def playerCollision(self): #Warp 클래스 안에 플레이어의 충돌판정을 위한 함수(메서드)를 만듭니다.
          if self.warp.intersects(player): #intersects 기능을 이용하여 조건문을 생성합니다.
               self.player.position = (95,3,90) #플레이어의 좌표를 이동시킵니다.

class MonsterX(Entity): #클래스 MonsterX를 생성합니다.
     def __init__(self,x,z): 
          super().__init__( #Entity 클래스의 속성을 그대로 가져와 enemy를 초기화합니다.
               enemy = Entity(
                    model = 'assets/enemy.obj',
                    texture = 'assets/EnemyTexture.png',
                    scale = 0.5,
                    position = (x * 5, 1, z * 5),
                    collider = 'box'
               )
          )
          self.player = player
          self.start = self.enemy.position

     def update(self):
          self.enemy.rotation_y = 90
          self.enemy.set_position((self.enemy.position.x + 5 * time.dt, self.enemy.position.y, self.enemy.position.z ))
          #객체의 좌표를 수정하여 움직임을 구현합니다.
          
          if self.enemy.intersects(player):
               self.player.position = (95, 3, 90)
          
          for i in walls:
               if self.enemy.intersects(i):
                    self.enemy.position = self.start


def input(key):
    if key == 'escape':
        application.quit()


#EditorCamera()
player = Player()


MAP =[
    [11,12,13,14,15,16,17,18,19,10,11,12,13,'e',15,16,17,18,19,20],
    [11,__,__,__,__,__,17,__,19,__,11,12,13,__,15,16,17,__,__,20],
    [11,__,13,14,15,__,__,__,__,__,__,__,13,__,15,__,17,__,19,20],
    [11,__,13,__,__,__,17,18,19,10,11,__,13,__,15,__,17,__,__,20],
    [11,__,13,14,15,__,17,__,__,__,11,__,13,__,__,__,__,__,__,20],
    [11,__,__,__,15,__,17,__,19,__,11,__,__,__,15,16,17,18,__,20],
    [11,12,13,__,__,__,17,__,19,__,11,12,13,14,15,16,__,__,__,20],
    [11,__,__,14,15,__,__,__,19,__,__,__,__,__,__,__,__,18,__,20],
    [11,__,13,__,15,16,17,18,19,__,11,12,13,14,15,16,17,18,__,20],
    [11,__,13,__,15,__,__,__,19,__,__,12,__,__,__,__,__,__,__,20],
    [11,__,__,__,__,__,17,__,19,10,11,__,__,14,15,16,17,18,19,20],
    [11,12,__,14,15,__,17,__,__,__,__,__,13,14,__,__,__,__,__,20],
    [11,__,__,14,15,__,__,18,19,10,11,12,13,__,__,16,__,18,__,20],
    [11,12,__,__,__,16,__,18,__,__,__,12,13,14,15,16,__,18,__,20],
    [11,12,__,14,__,16,__,18,__,10,__,__,__,__,__,__,__,18,__,20],
    [11,__,__,__,__,16,__,18,__,10,11,__,13,__,15,16,17,__,__,20],
    [11,12,__,14,15,16,__,__,__,10,__,12,__,__,15,16,17,18,__,20],
    [11,__,__,__,__,__,17,18,19,10,__,12,__,14,__,__,__,'x','e',20],
    [11,12,__,14,15,__,__,__,__,__,__,__,__,14,__,16,__,__,__,20],
    [11,12,13,14,15,16,17,18,19,10,11,12,13,14,15,16,17,18,'p',20],    
]

walls = [] # 생성된 wall 객체의 정보를 저장하기 위해 walls 배열을 생성합니다.

for i in range(len(MAP)):
    for j in range(len(MAP[i])):
            if MAP[i][j]:
                if MAP[i][j] == 'p':
                    player.position = (i * 5, 0, j * 5)
                    continue
                if MAP[i][j] == 'e':
                     exitdoor = Exit(i,j) # exitdoor 객체를 생성하고, Exit 클래스 호출하며 i, j 값 전달     
                     continue
                if MAP[i][j] == 'w': 
                     warpgate = Warp(i,j) # warpgate 객체를 생성하고, Exit 클래스 호출하며 i, j 값 전달     
                     continue
                if MAP[i][j] == 'x':
                     moster = MonsterX(i,j) # monster 객체를 생성하고, Exit 클래스 호출하며 i, j 값 전달     
                     continue

                wall = Entity(                
                    model = 'cube',
                    #color = color.black90,
                    position = (i * 5, 0, j * 5),
                    scale = (5,5,5),
                    collider = 'box',
                    texture = 'assets/WallTexture.jpg' # assets 폴더안 텍스처 사진을 불러옵니다.
               )
                walls.append(wall) #wall 객체의 정보를 walls 배열 안에 저장합니다.
         
Ground = Entity(
     model = 'plane',
     color = color.gray,
     position = (50,0,50),
     scale = (150,1,150),
     collider = 'mesh'
)

sky = Entity(
    model = 'sphere',
    position = (0,0,0),
    scale = (400,400,400),
    collider = 'mesh',
    texture = 'assets\stars.png',
    double_sided = True # 물체의 양면을 모두 렌더링합니다.

)


app.run()
