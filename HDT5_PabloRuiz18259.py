import simpy
import random

random.seed(1234567890)
numberOfProcesses = 25  #Defines the amount of processes to be executed
CPUprocesses = 3

def proceso(name, env, processTime, cpu, wait):

    # Waits for a RAM assignation
    yield env.timeout(processTime)

    timeReceived = env.now
    RAMQuantity = random.randint(1, 10)
    instructionNumber = random.randint(1, 10)
    print('%s llega a las %f necesita %d de memoria RAM y cuenta con %d instrucciones' %
          (name, timeReceived, RAMQuantity, instructionNumber))

    if(RAM.level >= RAMQuantity):
        RAM.get(RAMQuantity)
        print("%s READY" % name)
        print("Quedan %i de RAM" % RAM.level)



        with cpu.request() as turn:
            yield turn
            yield env.timeout(instructionNumber)
            print('%s sale a las %f del CPU' % (name, env.now))

    else:
        print("No hay suficiente RAM disponible, instruccion en cola")

    totalTime = env.now - timeReceived
    print('%s se tardo %f' % (name, totalTime))
    print()




env = simpy.Environment()   # Simulation environment
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)
WAITING = simpy.Resource(env, capacity=1)   # Queue of I/O


for i in range(numberOfProcesses):
    env.process(proceso("Instruccion %d" % i, env, random.expovariate(1.0 / 10), CPU, WAITING))


env.run(until=100)