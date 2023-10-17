import connection as cn
import processor
import numpy as np
import matplotlib.pyplot as plt
import handler
from rx import operators as ops
connection_=cn.connector()
process=processor.Processor()


vect_data=handler.Data_handler()
vect_transformed=handler.Data_handler()


Real_time_graph=connection_.data.pipe(ops.publish())
transform_data=connection_.data.pipe(ops.publish())

Real_time_graph.connect()
transform_data.connect()

transform_data.subscribe(process.add_data)#Datos para aplicarles fft
process.data.subscribe(vect_transformed.handler)#A los datos transformados los mando a otro vector

sub=Real_time_graph.subscribe(vect_data.handler)#Datos para plotear

cn.sleep(2)#Dejamos que se ejecute el hilo por n segundos
connection_.close()#Cerramos las conexiones
process.close()
sub.dispose()

print(str(len(vect_data.raw_data)))#Generamos el grafico de los datos sin procesar
x=np.arange(0,len(vect_data.raw_data))
y=np.array(vect_data.raw_data)
plt.plot(x,y)
plt.show()

print(str(len(vect_transformed.raw_data)))
#x=np.arange(0,len(vect_transformed.raw_data))#Generamos el grafico de los datos procesados
#y=np.array(vect_transformed.raw_data)
plt.plot(vect_transformed.raw_data)
plt.show


