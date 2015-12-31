#! /usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from machinekit import hal

cname = 'mk_jointstate'
topic = 'mk_jointstate'

# maps msg types to HAL types
pintypes = {
    'float32' : hal.HAL_FLOAT,
    'float64' : hal.HAL_FLOAT,
    'int32' :   hal.HAL_S32,
    'uint32' :  hal.HAL_U32,
    'bool' :    hal.HAL_BIT
}

arraytypes = {
    'float32[]' : 'float32',
    'float64[]' : 'float64',
    'int32[]' :   'int32',
    'uint32[]' :  'uint32'
}

def gen_halcomp(name, topic, msgtype, dir ):
    ''' define a HAL component whose pins match msg field names and types '''
    c = hal.Component(name)
    c.newpin('test2', hal.HAL_FLOAT, hal.HAL_IN)
    msg = msgtype()
    pins = dict()
    for i in range(len(msg.__slots__)):
        # check the attributes for types and if they are of an array type
        # then iterate over them, if not, than ignore them.
        fname = msg.__slots__[i]
        ftype = msg._slot_types[i]
        if ftype in arraytypes:
            #iterate an array of supported types
            for j in range(len(fname)):
                #ptype = fname._slot_types[j]#arraytypes[ftype]
                #print("pin type = %s") % (ptype)
                pname = "%s.%s.%s" % (topic, fname, j)
                print("pin name = %s") % (pname)
                pins[pname] = c.newpin(pname, hal.HAL_FLOAT, dir)
        else:
            if not ftype in pintypes:
                print("type %s not supported... ignoring this type") % ftype
            else:
                pname = "%s.%s" % (topic, fname)
                print("pin name = %s") % (pname)
                pins[pname] = c.newpin(pname, pintypes[ftype], dir)
    print("c.ready()")
    c.ready()
    return pins

#def talker(pins, cname, topic, msgtype, rate):
#    ''' publish the pins in comp '''
#    rospy.init_node(cname, anonymous=True)
#    pub = rospy.Publisher(cname + "/" + topic, msgtype, queue_size=10)
#    r = rospy.Rate(rate)
#    msg = msgtype()
#    while not rospy.is_shutdown():
#        for i in range(len(msg.__slots__)):
#            fname = msg.__slots__[i]
##            msg.__setattr__(fname, pins[fname].get())
#            print("type == %s") % (ftype)
#        pub.publish(msg)
#        r.sleep()

if __name__ == '__main__':
    c = hal.Component('test')
    c.newpin('test', hal.HAL_FLOAT, hal.HAL_IN)
    pins = gen_halcomp(cname, topic, JointState, hal.HAL_IN)
#    gen_halcomp(cname, topic, JointState, hal.HAL_IN)
#    try:
#        talker(pins, cname, topic, JointState, 10)
#    except rospy.ROSInterruptException: pass
