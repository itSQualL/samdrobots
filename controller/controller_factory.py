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
    def __init__(self):
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
        return controller_prx

    def makeDetectorController(self, current):
        """
        Pending implementation:
        DetectorController* makeDetectorController();
        """
        print("Make detector controller.")

        if self.detector_controller is not None:
            return self.detector_controller

        controller = DetectorControllerI()
        object_prx = current.adapter.addWithUUID(controller)
        self.detector_controller = \
            drobots.DetectorControllerPrx.checkedCast(object_prx)
        return self.detector_controller

    def amountCreated(self, current=None):
        return self.controllers

class RobotControllerAttacker(drobots.RobotController):
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
        self.disparos = 0
        self.location = self.bot.location()
        self.angulo = 0
        self.estado = 1



    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        print("\n*****************************")
        print("******TURNO "+str(self.turno) +" ATTACKER******")
        print("*****************************\n")

        print("Soy: " + str(id(self)))

        print("Posicion: X = {}, Y = {}".format(self.location.x, self.location.y))

        for i in range(2):
            if (self.disparos<8):
                print("voy a hacer mi disparo " + str(self.disparos) )
                if (self.disparos==0):
                    self.angulo = 0
                    self.disparar()
                    self.disparos += 1
                else:
                    self.angulo += 45
                    self.disparar()
                    self.disparos += 1
            else:
                print("reinicio disparos")
                self.disparos=0
                self.move()
                break


        print("*********FIN TURNO "+str(self.turno) + " ATTACKER*********\n")
        self.turno += 1

    def move(self):
        location=self.bot.location();
        
        if(location.x>390 and location.y<10):
            self.bot.drive(225,100)
            print("Se supone que me muevo con angulo: 225 velocidad: 100")
        elif(location.x<10 and location.y<10):
            self.bot.drive(315,100)
            print("Se supone que me muevo con angulo: 315 velocidad: 100")
        elif(location.y>390 and location.x<10):
            self.bot.drive(45,100)
            print("Se supone que me muevo con angulo: 45 velocidad: 100")
        elif(location.y>390 and location.x>390):
            self.bot.drive(135,100)
            print("Se supone que me muevo con angulo: 135 velocidad: 100")
        else:
            self.bot.drive(random.randint(0,359),100)
            print("Se supone que me muevo con angulo: random velocidad: 100")

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
        
        self.bot.cannon(self.angulo,81)

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        self.estado = 0
        print("Robot ATTACKER murio\n")
        pass


class RobotControllerDefender(drobots.RobotController):
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
        
        if(location.x>350 and location.y<50):
            self.bot.drive(225,100)
            print("Se supone que me muevo con angulo: 225 velocidad: 100")
        elif(location.x<50 and location.y<50):
            self.bot.drive(315,100)
            print("Se supone que me muevo con angulo: 315 velocidad: 100")
        elif(location.y>350 and location.x<50):
            self.bot.drive(45,100)
            print("Se supone que me muevo con angulo: 45 velocidad: 100")
        elif(location.y>350 and location.x>350):
            self.bot.drive(135,100)
            print("Se supone que me muevo con angulo: 135 velocidad: 100")
        else:
            self.bot.drive(random.randint(0,359),100)
            print("Se supone que me muevo con angulo: random velocidad: 100")


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



class DetectorControllerI(drobots.DetectorController):
    """
    DetectorController interface implementation.

    It implements the alert method.

    Remember: every alert call will include de position, so there is no need
    to create a DetectorControllerI servant for every detector, you can re-use
    the same servant (and its proxy) to every "makeDetectorController" petition
    on the PlayerI
    """
    def alert(self, pos, robots_detected, current):
        """
        Method that receives a Point with the coordinates where the detector is
        placed and the number of robots around it. This method is only invoked
        when at least 1 robot is near to the detector. If there is no robots
        around it, this method will never be called.
        """
        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))
