import connection as cn
import processor
import numpy as np
import matplotlib.pyplot as plt
import handler
from rx import operators as ops
connection_=cn.connector()
process=processor.Processor()
vect_data=handler.Data_handler()



Real_time_graph=connection_.data.pipe(ops.share())
#transform_data=connection_.data.pipe(ops.share())

#transform_data.subscribe(process.add_data)
sub=Real_time_graph.subscribe(vect_data.handler)
cn.sleep(5)
connection_.close()
process.close()
sub.dispose()
print(str(len(vect_data.raw_data)))
x=np.arange(0,len(vect_data.raw_data))
y=np.array(vect_data.raw_data)
plt.plot(x,y)
plt.show()



