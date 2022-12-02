import numpy as np
import random

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer

from SimpleContinuousModule import SimpleCanvas

class Car(Agent):
    def __init__(self, model: Model, pos, speed, horizontal = False, north = False, east = False):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.speed = speed
        self.horizontal = horizontal
        self.north = north
        self.east = east

    def step(self):
        # Agente Volantazo en rango
        try:
            agent = self.valTurn() #regresa agente Volantazo
            # print(agent.turn)
            # print(self.pos[0], self.pos[1])
            if self.pos[0] > 13 and not self.horizontal and agent.turn and agent.pos[1] > 13 and self.north:
                self.horizontal = True
                self.east = True
                self.north = False
            elif self.pos[0] < 11 and not self.horizontal and agent.turn and agent.pos[1] < 11 and not self.north:
                self.horizontal = True
                self.east = False
                self.north = True
            elif self.pos[0] > 13 and self.horizontal and agent.turn and agent.pos[1] < 11 and not self.east:
                self.horizontal = False
                self.north = True
                self.east = True
            elif self.pos[0] < 11 and self.horizontal and agent.turn and agent.pos[1] > 13 and self.east:
                self.horizontal = False
                self.north = False
                self.east = False
        except:
            pass
        # car_ahead = self.car_ahead()
        # car_side =  self.car_side()
        if not self.horizontal and not self.valLight():
            self.vertical_step()
        elif self.horizontal and not self.valLight():
            self.horizontal_step()
        # else:
        #     self.decelerate()
        
      
    def vertical_step(self):
        car_ahead = self.car_ahead()
        car_side =  self.car_side()

        if car_ahead == None and car_side == None:
            new_speed = self.accelerate()
        else:
            new_speed = self.decelerate()

        if new_speed >= 1.5:
            new_speed = 1.5
        elif new_speed <= -1.5:
            new_speed = -1.5

        self.speed = np.array([0.0, new_speed])
        new_pos = self.pos + np.array([0.0, 0.3]) * self.speed    
        self.model.space.move_agent(self, new_pos)

    def horizontal_step(self):
        car_ahead = self.car_ahead()
        car_side =  self.car_side()
        if car_ahead == None and car_side == None: 
            new_speed = self.accelerate()
        else:
            new_speed = self.decelerate()

        if new_speed >= 1.5:
            new_speed = 1.5
        elif new_speed <= -1.5:
            new_speed = -1.5

        self.speed = np.array([new_speed, 0.0])
        new_pos = self.pos + np.array([0.3, 0.0]) * self.speed
        self.model.space.move_agent(self, new_pos)


    def valLight(self):
        for agent in self.model.space.get_neighbors(self.pos, 1):
            if isinstance(agent, Tlight) and not agent.status: #luz en rojo
                self.speed = (0.0, 0.0)
                return True
            elif self.horizontal and self.east:
                self.speed = (1.0, 0.0)
            elif self.horizontal and not self.east:
                self.speed = (-1.0, 0.0)
            elif not self.horizontal and not self.north:
                self.speed = (0.0, 1.0)
            else:
                self.speed = (0.0, -1.0)

        return False
    
    def valTurn(self):
        for agent in self.model.space.get_neighbors(self.pos, .15):
            if isinstance(agent, Volantazo):
                turn = random.choice([True, False])
                agent.turn = turn
                return agent

    def car_ahead(self):
        for neighbor in self.model.space.get_neighbors(self.pos, 2, False):
            # if self.north and not self.horizontal and self.pos[1] > neighbor.pos[1] and not isinstance(neighbor, Volantazo) and not isinstance(neighbor,Tlight):
            #     print("North")
            #     return neighbor
            # elif not self.north and not self.horizontal and self.pos[1] < neighbor.pos[1] and not isinstance(neighbor, Volantazo) and not isinstance(neighbor,Tlight):
            #     print("South")
            #     return neighbor


            if not self.north and not self.horizontal and self.pos[1] < neighbor.pos[1] and isinstance(neighbor, Car):
                print("South")
                return neighbor
            elif self.east and self.horizontal and self.pos[0] < neighbor.pos[0] and isinstance(neighbor, Car):
                print("Este")
                return neighbor
            
        return None

    def car_side(self):
        for neighbor in self.model.space.get_neighbors(self.pos, 2, False):
            # print(self.east, self.pos[0], neighbor.pos[0])
            # if self.east and self.horizontal and self.pos[0] < neighbor.pos[0] and not isinstance(neighbor, Volantazo) and not isinstance(neighbor,Tlight):
            #     print("Este")
            #     return neighbor
            # elif not self.east and self.horizontal and self.pos[0] > neighbor.pos[0] and not isinstance(neighbor, Volantazo) and not isinstance(neighbor,Tlight):
            #     print("West")
            #     return neighbor
            
            if self.north and not self.horizontal and self.pos[1] > neighbor.pos[1] and isinstance(neighbor, Car):
                print("North")
                return neighbor
            elif not self.east and self.horizontal and self.pos[0] > neighbor.pos[0] and isinstance(neighbor, Car):
                print("West")
                return neighbor

        return None

    def accelerate(self):
        if self.horizontal and self.east:
            return self.speed[0] + 0.05
        elif self.horizontal and not self.east:
            return self.speed[0] - 0.05
        elif not self.horizontal and not self.north:
            return self.speed[1] + 0.05
        else:
            return self.speed[1] - 0.05

    def decelerate(self):
        if self.horizontal and self.east:
            return self.speed[0] * 0
        elif self.horizontal and not self.east:
            return self.speed[0] * 0
        elif not self.horizontal and not self.north:
            return self.speed[1] * 0
        else:
            return self.speed[1] * 0

class Volantazo(Agent):
    def __init__(self, model: Model, pos,  turn = False):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.turn = turn


class Tlight(Agent):
    def __init__(self, model:Model, status = False, counter = 0):
        super().__init__(model.next_id(), model)
        self.status = status
        self.counter = counter
    def step(self):
        if self.counter == 160:
            self.counter = 0
        if self.counter == 0 and not self.status:
            self.status = True
        if self.counter == 40 and self.status:
            self.status = False

        if self.counter < 160:
            self.counter += 1


class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 25, True)
        self.schedule = RandomActivation(self)
        # self.schedule = BaseScheduler(self)

        # Volantazo
        volantazo1 = Volantazo(self, (10, 10), False)
        self.space.place_agent(volantazo1, volantazo1.pos)
        self.schedule.add(volantazo1)

        volantazo2 = Volantazo(self, (14, 10), False)
        self.space.place_agent(volantazo2, volantazo2.pos)
        self.schedule.add(volantazo2)

        volantazo3 = Volantazo(self, (10,14), False )
        self.space.place_agent(volantazo3, volantazo3.pos)
        self.schedule.add(volantazo3)

        volantazo4 = Volantazo(self, (14, 14), False)
        self.space.place_agent(volantazo4, volantazo4.pos)
        self.schedule.add(volantazo4)


        # Cars
        car1 = Car(self, np.array([10, 6]), np.array([0.0, 1.0]), False, False, False)
        self.space.place_agent(car1, car1.pos)
        self.schedule.add(car1)

        car2 = Car(self, np.array([14, 24]), np.array([0.0, -1.0]), False, True, False)
        self.space.place_agent(car2, car2.pos)
        self.schedule.add(car2)

        car3 = Car(self, np.array([1, 14]), np.array([1.0, 0.0]), True, False, True)
        self.space.place_agent(car3, car3.pos)
        self.schedule.add(car3)

        car4 = Car(self, np.array([24, 10]), np.array([-1.0, 0.0]), True, False, False)
        self.space.place_agent(car4, car4.pos)
        self.schedule.add(car4)

        # Tlights
        light1 = Tlight(self, False, 0)
        self.space.place_agent(light1, (10.5, 8))
        self.schedule.add(light1)

        light2 = Tlight(self, False, 40)
        self.space.place_agent(light2, (16, 10.5))
        self.schedule.add(light2)

        light3 = Tlight(self, False, 80)
        self.space.place_agent(light3, (13.5, 16))
        self.schedule.add(light3)

        light4 = Tlight(self, False,120)
        self.space.place_agent(light4, (8, 13.5))
        self.schedule.add(light4)

    def step(self):
        self.schedule.step()

    def getCarros(self):
        carros = []
        for n in self.schedule.agents:
            if isinstance(n, Car):
                carros.append({"id": n.unique_id, "pos": [n.pos[0], n.pos[1]], "horizontal":n.horizontal, "north":n.north, "east":n.east}) 
        return carros
    
    def getSemaforos(self):
        semaforos = []
        for n in self.schedule.agents:
            if isinstance(n, Tlight):
                semaforos.append({"id": n.unique_id, "pos": [n.pos[0], n.pos[1]], "estatus": n.status}) 
        return semaforos

    def getVolantazos(self):
        volantazos = []
        for n in self.schedule.agents:
            if isinstance(n, Volantazo):
                volantazos.append({"id": n.unique_id, "pos": [n.pos[0], n.pos[1]], "turn": n.turn}) 
        return volantazos


# def draw(agent):
#     color = "Blue" if agent.unique_id == 1 else "Brown"
#     if isinstance(agent, Volantazo):
#         return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Gray"}
#     if isinstance(agent, Tlight) and not agent.status:
#         return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Red"}
#     if isinstance(agent, Tlight) and agent.status:
#         return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Green"}
#     if isinstance(agent, Car) and agent.horizontal:
#         return {"Shape": "rect", "w": 0.04, "h": 0.03, "Filled": "true", "Color": color}
#     if isinstance(agent, Car) and not agent.horizontal:
#         return {"Shape": "rect", "w": 0.03, "h": 0.04, "Filled": "true", "Color": color}



# canvas = SimpleCanvas(draw, 500, 500)

# model_params = {}

# server = ModularServer(Street, [canvas], "Traffic", model_params)
# server.port = 8254
# server.launch()
