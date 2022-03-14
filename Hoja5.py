import simpy
import random
import statistics

lista = []
random.seed(50)
env = simpy.Environment()  
initial_ram = simpy.Container(env, 100, init=100) 
initial_cpu = simpy.Resource(env, capacity=2)
cant_proces = 3        #velocidad
initial_procesos = 150 #cantidad
tiempo_total = 0
intervalo = 1

def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram):
    yield env.timeout(llegada)
    tiempo_llegada = env.now
    
    yield memoria.get(cantidad_ram)
    print('%s proceso en cola [NEW llegada] -> %d cantidad ram requerida %d, disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    
    
    while (cantidad_instrucciones > 0):
        print('%s proceso en cola READY tiempo -> %d cantidad instrucciones pendientes %d' % (nombre, env.now, cantidad_instrucciones))
        with cpu.request() as req:  
            yield req
            cantidad_instrucciones = cantidad_instrucciones - cant_proces
            yield env.timeout(1) 
            print('%s proceso en estado RUNNING fue atendido en tiempo -> %d cantidad ram %d, Instrucciones pendientes %d ram disponible %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))
        
        if (cantidad_instrucciones > 0):
            waiting_ready = random.randint(1,2)
            if (waiting_ready == 1):
                print("[WAITING] %s esta realizando operaciones I/O en tiempo actual de: %d" %(nombre, env.now))
                yield env.timeout(1)
            
    yield memoria.put(cantidad_ram)

    print('%s proceso TERMINATED salida -> %d cantidad ram devuelta %d, nueva cantidad de memoria disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    global tiempo_total
    lista.append(env.now)
    tiempo_total += env.now - tiempo_llegada
    print('Tiempo total %f' % (env.now - tiempo_llegada))
    #fin de proceso ---------------------------------

for i in range(initial_procesos):
    llegada = random.expovariate(1.0 / intervalo)
    cantidad_instrucciones = random.randint(1, 10)  
    UsoRam = random.randint(1, 10)  
    env.process(proceso('proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))


env.run()
print('tiempo promedio %f ' % (tiempo_total / initial_procesos))
print('desviacion estandard %f ' % (statistics.pstdev(lista)))
