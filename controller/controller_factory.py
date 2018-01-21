import Ice
Ice.loadSlice('-I. --all ./interfaces/services.ice')

import drobots
import services
import random
import math

class ControllerFactoryI(services.ControllerFactory):
    """
    ControllerFactory interface implementation
    """
    def __init__(self, container_prx):
        self.container_prx = container_prx
        self.detector_controller = None
        self.controllers = 0
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

    def makeController(self, bot, current=None):
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

        """
        makeController is invoked by the game server. The method receives a
        "bot", instance of RobotPrx.

        It is mandatory to return a direct proxy, in case that you are using
        IceGrid
        """

        print("Make controller received bot {}".format(bot))
        if bot.ice_isA("::drobots::Attacker"):
            controller = RobotControllerAttacker(bot, self.mines)
            object_prx = current.adapter.addWithUUID(controller)
            controller_prx = drobots.RobotControllerPrx.checkedCast(object_prx)

        elif(bot.ice_isA("::drobots::Defender")):
            controller = RobotControllerDefender(bot, self.mines)
            object_prx = current.adapter.addWithUUID(controller)
            controller_prx = drobots.RobotControllerPrx.checkedCast(object_prx)

        self.controllers += 1
        self._set_bot_prx(controller_prx)
        return controller_prx

    def _set_bot_prx(self, controller_prx):
        container_list = self.container_prx.list()
        if not "bot_0" in container_list:
            self.container_prx.link("bot_0", controller_prx)
        elif not "bot_1" in container_list:
            self.container_prx.link("bot_1", controller_prx)
        elif not "bot_2" in container_list:
            self.container_prx.link("bot_2", controller_prx)
        elif not "bot_3" in container_list:
            self.container_prx.link("bot_3", controller_prx)

    def makeDetectorController(self, current):
        """
        Pending implementation:
        DetectorController* makeDetectorController();
        """
        print("Make detector controller.")

        if self.detector_controller is not None:
            return self.detector_controller

        controller = DetectorControllerI(self.container_prx)
        object_prx = current.adapter.addWithUUID(controller)
        self.detector_controller = \
            drobots.DetectorControllerPrx.checkedCast(object_prx)
        return self.detector_controller

    def amountCreated(self, current=None):
        return self.controllers

class RobotControllerAttacker(services.ControllerCommunication):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, mines):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        print("CREADO ROBOT ATTACKER")
        self.turno = 0
        self.bot = bot
        self.mines = mines
        self.turnDetector=0
        self.location = self.bot.location()
        self.angulo = 0
        self.estado = 1
        self.detector = {}
        self.bool = False
        self.lastAlert = None
        self.enemiesAux=0
        self.center=False
        #self.alert_enemies = [0,0,0,0]


    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with our Robot
        """
        print("\n*****************************")
        print("******TURNO "+str(self.turno) +" ATTACKER******")
        print("*****************************\n")

        print("Soy: " + str(id(self)))

        print("Posicion: X = {}, Y = {}".format(self.location.x, self.location.y))


        if(self.bool==True):
            self.turnDetector+=1
            for i in range(2):
                dist=self.calcularDistancia()
                print("SALGO DE CALCULAR DISTANCIA dist = " +str(dist))
                if(dist<=80):
                    print("¡¡¡¡¡¡ME VOY A ALEJAR!!!!!!")
                    self.move(self.location.x,self.location.y,self.lastAlert.x,self.lastAlert.y)
                    self.turnDetector-=1
                    break
                else:
                    print("VOY A DISPARAR AL DETECTOR. Disparo numero " + str(self.turnDetector))
                    self.dispararDetector(dist,self.lastAlert.x,self.lastAlert.y,self.location.x,self.location.y)
                    

                    if(self.turnDetector==2):
                        self.bool=False
                        self.turnDetector=0 
                    print(" despues de atacar " + str(self.turnDetector) + "vez, el boolean esta a " + str(self.bool)) 
                  

        else:
            if(self.center==False):

                location=self.bot.location();
                self.move(200,200,location.x,location.y)
                if(self.location.x>=185 and self.location.x<=215 and self.location.y>=185 and self.location.y<=215):
                    self.center=True
                    self.bot.drive(0,0)
            else:
                for i in range(2):
                    print("voy a hacer mi disparo. PAYUN!")
                    if (self.angulo==360):
                        self.angulo = 0
                        self.disparar()
                        self.angulo += 45
                    else:
                        self.disparar()
                        self.angulo += 45


        print("*********FIN TURNO "+str(self.turno) + " ATTACKER*********\n")
        self.turno += 1

    def calcularDistancia(self):

        detectorX=self.lastAlert.x
        detectorY=self.lastAlert.y

        m=math.sqrt( ( math.pow( (detectorX-self.location.x) ,2)) + ( math.pow( (detectorY-self.location.y) ,2)) )
        m=math.ceil(m)
        print("Distancia calculada " + str(m))
        return m

    def dispararDetector(self, dist,centerX,centerY, pointX, pointY):
        angulo = self.calcularAngulo(centerX,centerY, pointX, pointY)
        print("Voy a disparar al angulo " + str(angulo))
        self.bot.cannon(angulo,dist)



    def calcularAngulo(self, centerX,centerY, pointX, pointY):
        m=(centerY - pointY) / (centerX - pointX)
        rad=math.atan(m)
        angulo = math.degrees(rad)

        if(angulo<0):
            angulo+=360
        if(pointX>centerX and pointY<centerY):
            angulo-=180
        elif(pointX>centerX and pointY>centerY):
            angulo+=180
        print("Angulo calculado " +str(angulo))
        angulo=abs(angulo)

        return angulo

    def move(self, centerX,centerY, pointX, pointY):
        
        if(pointX==centerX):
            if(pointY<=centerY):
                angulo=90
            else:
                angulo=270
        else:
            angulo = self.calcularAngulo(centerX,centerY, pointX, pointY)

        print("\nVoy hacia el centro con angulo " + str(angulo))
        self.bot.drive(angulo,100);



        self.location =self.bot.location()


    def disparar(self):
        
        if (self.location.x <= 200):
            if (self.location.y <= 200):
                print("voy a disparar a cuadrante 1 con x=" + str(self.location.x) + " y=" + str(self.location.y) +"\n")
                if (self.location.x <= self.location.y):
                    distancia = self.location.x/2
                else:
                    distancia = self.location.y/2
            else:
                print("voy a disparar a cuadrante 2 con x=" + str(self.location.x) + " y=" + str(self.location.y) +"\n")
                auxY = 400 - self.location.y
                if (self.location.x <= auxY):
                    distancia = self.location.x/2
                    
                else:
                    distancia = auxY/2
        else:
            auxX = 400 - self.location.x
            if (self.location.y <= 200):
                print("voy a disparar a cuadrante 3 con x=" + str(self.location.x) + " y=" + str(self.location.y) +"\n")
                if (auxX <= self.location.y):
                    distancia = auxX/2
                else:
                    distancia = self.location.y/2
            else:
                print("voy a disparar a cuadrante 4 con x=" + str(self.location.x) + " y=" + str(self.location.y) +"\n")
                auxY = 400 - self.location.y
                if (auxX <= auxY):
                    distancia = auxX/2
                else:
                    distancia = auxY/2
        
        self.bot.cannon(self.angulo,111)

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        self.estado = 0
        print("Robot ATTACKER murio\n")
        pass

    def setEnemiesAlert(self, position, enemies, current=None):
        
        if str(position) in self.detector:
            enemiesAux = self.detector[str(position)]
            print("\nEl detector tiene a " +str(enemiesAux))
        else:
            enemiesAux=0            
            print("PRIMERA VEZ QUE VEO A ESTE SEÑOR")

        self.detector[str(position)] = enemies
        print("El detector tiene a " + str(self.detector[str(position)]))
        self.lastAlert=position

        print("Enemigos antes " +str(enemiesAux))
        print("Enemigos ahora " +str(self.detector[str(position)]))

        print(" antes de asignar el boolean esta a " + str(self.bool))
        if(self.bool==False):
            if(enemiesAux<self.detector[str(position)]):
                self.bool=True
            else:
                self.bool=False
        print(" despues de asignar el boolean esta a " + str(self.bool))


        print (str(self.detector))

class RobotControllerDefender(services.ControllerCommunication):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, mines):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        print("CREADO ROBOT DEFENDER")
        self.bot = bot
        self.mines = mines
        self.turno = 0
        self.detector = {}


    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        print("\n*****************************")
        print("******TURNO "+str(self.turno) +" DEFENDER******")
        print("****************************\n")


        

        location = self.bot.location()
        print("Posicion: X = {}, Y = {}".format(location.x, location.y))

        
        if(self.bot.energy()>10):
            self.escanear()
        if(self.bot.energy()>60):
            self.move(location)

        print("*********FIN TURNO "+str(self.turno) + " DEFENDER*********\n")
        self.turno+=1

    def move(self, location):
        location=self.bot.location();
        if(location.x>350):
            if(location.y<=50):
                self.bot.drive(135,100)
                print("Moviendo robot con alguno=135 velocidad=100")
            elif(location.y>50 and location.y<=350):
                self.bot.drive(180,100)
                print("Moviendo robot con alguno=180 velocidad=100")
            elif(location.y>350):
                self.bot.drive(215,100)
                print("Moviendo robot con alguno=135 velocidad=100")

        elif(location.x<50):
            if(location.y<=50):
                self.bot.drive(45,100)
                print("Moviendo robot con alguno=45 velocidad=100")
            elif(location.y>50 and location.y<=350):
                self.bot.drive(0,100)
                print("Moviendo robot con alguno=0 velocidad=100")
            elif(location.y>350):
                self.bot.drive(315,100)
                print("Moviendo robot con alguno=315 velocidad=100")
        if(location.y<50 and location.x>50 and location.x<350):
            self.bot.drive(90,100)
            print("Moviendo robot con alguno=90 velocidad=100")
        elif(location.y>350 and location.x>50 and location.x<350):
            self.bot.drive(270,100)
            print("Moviendo robot con alguno=270 velocidad=100")

    def escanear(self):
        angulo = random.randint(0,360)
        enemies = self.bot.scan(angulo,20)

        if enemies != 0:
            print("He encontrado enemigos, me vuevo en direccion contraria")
            if (angulo >= 180):
                angulo -=180
            else:
                angulo+=180

            self.bot.drive(angulo,100)


    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        print("El robot ha muerto\n")
        pass

    def setEnemiesAlert(self, position, enemies, current=None):
        self.detector[str(position)] = enemies
        print (str(self.detector))

class DetectorControllerI(drobots.DetectorController):
    """
    DetectorController interface implementation.

    It implements the alert method.

    Remember: every alert call will include de position, so there is no need
    to create a DetectorControllerI servant for every detector, you can re-use
    the same servant (and its proxy) to every "makeDetectorController" petition
    on the PlayerI
    """
    def __init__(self, container_prx):
        self.container_prx = container_prx

    def alert(self, pos, robots_detected, current):
        """
        Method that receives a Point with the coordinates where the detector is
        placed and the number of robots around it. This method is only invoked
        when at least 1 robot is near to the detector. If there is no robots
        around it, this method will never be called.
        """
        container_list = self.container_prx.list()

        bot_0_prx = container_list["bot_0"]
        bot_0_prx = services.ControllerCommunicationPrx.checkedCast(bot_0_prx)
        bot_0_prx.setEnemiesAlert(pos, robots_detected)

        bot_1_prx = container_list["bot_1"]
        bot_1_prx = services.ControllerCommunicationPrx.checkedCast(bot_1_prx)
        bot_1_prx.setEnemiesAlert(pos, robots_detected)

        bot_2_prx = container_list["bot_2"]
        bot_2_prx = services.ControllerCommunicationPrx.checkedCast(bot_2_prx)
        bot_2_prx.setEnemiesAlert(pos, robots_detected)

        bot_3_prx = container_list["bot_3"]
        bot_3_prx = services.ControllerCommunicationPrx.checkedCast(bot_3_prx)
        bot_3_prx.setEnemiesAlert(pos, robots_detected)

        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))
