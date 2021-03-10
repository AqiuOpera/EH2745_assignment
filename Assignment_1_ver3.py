# This python program is an algorithm to reading and parsing CIM-XML files and
# identify the grids topology and create a internal datastrucutre that
# represents a model of the grid.
# EH2745 Computer Applications in power systems course at KTH
# Author: Ziyao Wang, ziyaow@kth.se 
# Date: 2020-04-19
"""
Created on Sun Apr 19 19:41:51 2020

@author: Ziyao Wang
"""


# import library
import xml.etree.ElementTree as ET
import random
import pandapower as pp
from pandapower.plotting import simple_plot

# read XML file
treeEQ = ET.parse('Assignment_EQ_reduced.xml')
treeSSH = ET.parse('Assignment_SSH_reduced.xml')

# We can access the root of the tree
gridEQ = treeEQ.getroot()
gridSSH = treeSSH.getroot()

# To make working with the file easier, it may be useful to store the 
# namespace identifiers in strings and reuse when you search for tags
    
ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}


# get the name of equipment in the XML file
for equipment in gridEQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}","")
        # print(name)

# create CIM objects class which contains different information


# connectivitynode class: connectivitynodename, rdf id, type, container id, TE 
# list, base voltage and attached number.
class Connectivity_node:
  def __init__(self, x):
    self.name = name
    self.rdf_id = 'null'
    self.type = 'null'
    self.container_id = 'null'
    self.basevoltage = 0
    self.Terminal_list = []
    self.CE_type = 'null'
    self.bus = 'null'
    self.num_attachTerms = 0
    self.tr_hv_bus = 'null'
    self.tr_lv_bus = 'null'
    
    
# terminal class: terminal rdf id, terminal name, conducting equipment id, 
# connectivitynode id and node type
class Terminal:
  def __init__(self, x):
    self.name = name
    self.rdf_id = 'null'
    self.type = 'null'
    self.CN_rdf_id = 'null'
    self.CE_rdf_id = 'null'
    self.CE_type = 'null'
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.traversal_flag = 1
    
    
# conducting equipment class: conducting equipment name, rdf id, node type, 
# conducting equipment type and base voltage
class Conducting_equipment:
  def __init__(self, x):
    self.name = name
    self.rdf_id = 'null'
    self.type = 'null'
    self.CE_type = 'null'
    self.Terminal_list = []
    self.basevoltage = 0
    self.num_attachTerms = 0 
    
    
# create Busbranch objects class which contains different information
    
# busbar section class: basbar section name, rdf id, equipment container id
# node type and busbar base voltage.
class Busbar_section:
  def __init__(self, x):
    self.name = name
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.type = 'null'
    self.CE_type = 'null'
    self.basevoltage = 0
    self.equipmentcontainer_rdf_id = 'null'
    self.type = 'CE'
    self.rdf_id = 'null'
    self.bus = 'null'
    
 
# energy consumer load class: energy consumer load id, energy consumer load
# name, active power, reactive power, equipment container id and base voltage
# id.
class Energy_consumer_load:
  def __init__(self, x):
    self.name = name
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.CE_type = 'null'
    self.type = 'CE'
    self.rdf_id = 'null'
    
    
# synchronous machine class: synchronous machine id, synchronous machine name,
# rated power, active power, reactive power,generator unit id, regulating
# control id, equipment control id and base voltage id.
class Synchronous_machine:
  def __init__(self, x):
    self.name = name  
    self.Terminal_list = []
    self.CE_type = 'null'
    self.num_attachTerms = 0 
    self.type = 'CE'
    self.rdf_id = 'null'


# class AC line segment: AC line id, AC line name, equipment container, AC line
# segment rground, AC line segment xground, AC line segment bch, AC line
# segment gch, AC line length and AC line base voltage id.
class AC_Line_segment:
  def __init__(self, x):
    self.name = name
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.CE_type = 'null'
    self.type = 'CE'
    self.rdf_id = 'null'
    
    
# power transformer class: power transformer id, power transformer name and
# equipment container id.
class Power_transformer:
  def __init__(self, x):
    self.name = name
    self.CE_type = 'null'
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.type = 'CE'
    self.rdf_id = 'null'
      
    
# breaker class: breaker id, breaker name, breaker state, equipment container
# id and base voltage id.
class Breaker:
  def __init__(self, x):
    self.name = name
    self.Terminal_list = []
    self.num_attachTerms = 0 
    self.CE_type = 'null'
    self.type = 'CE'
    self.rdf_id = 'null'
    self.breakeropen = 'false'


# line shunt compensator class: line shunt compensator id, line shunt
# compensator name, line shunt compensator bpersection, line shunt compensator
# gpersection, equipment container, base voltage id and base voltage value.
class Linear_shunt_compensator:
  def __init__(self, x):
    self.name = name
    self.Terminal_list = []
    self.num_attachTerms = 0
    self.CE_type = 'null'
    self.type = 'CE'
    self.rdf_id = 'null'


# Initialize the lists
connectivity_node_list = []
terminal_list = []
conducting_equipment_list = []
node_list = []

busbar_section_list = []
energy_consumer_load_list = []
synchronous_machine_list = []
AC_line_segment_list = []
power_transformer_list = []
breaker_list = []
linear_shunt_compensator_list = []


# get the information from XML file and store it in the lists
for equipment in gridEQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}","")
        # connectivity node list
        if name == 'ConnectivityNode':
            connectivity_node = Connectivity_node(equipment)
            connectivity_node.name = equipment.find('cim:IdentifiedObject.name',ns).text
            connectivity_node.type = 'CN'
            connectivity_node.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
            connectivity_node.container_id = equipment.find('cim:ConnectivityNode.ConnectivityNodeContainer',ns).attrib.get(ns['rdf']+'resource')
            for voltagelevel in gridEQ.findall('cim:VoltageLevel',ns):
                if voltagelevel.attrib.get(ns['rdf']+'ID') == connectivity_node.container_id.replace("#", "") :
                    basevoltage_id = voltagelevel.find('cim:VoltageLevel.BaseVoltage',ns).attrib.get(ns['rdf']+'resource')
                    for Basevoltage in gridEQ.findall('cim:BaseVoltage',ns):
                        if Basevoltage.attrib.get(ns['rdf']+'ID') == basevoltage_id.replace("#", "") :
                            connectivity_node.basevoltage = float(Basevoltage.find('cim:BaseVoltage.nominalVoltage',ns).text)
            connectivity_node_list.append(connectivity_node)
            node_list.append(connectivity_node)
            
        
        # terminal list
        elif name == 'Terminal':
            terminal = Terminal(equipment)
            terminal.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
            terminal.type = 'TE'
            terminal.CN_rdf_id = equipment.find('cim:Terminal.ConnectivityNode',ns).attrib.get(ns['rdf']+'resource')
            terminal.CE_rdf_id = equipment.find('cim:Terminal.ConductingEquipment',ns).attrib.get(ns['rdf']+'resource')
            terminal.traversal_flag = 0
            terminal_list.append(terminal)
            node_list.append(terminal) 
            
        
        # conducting equipment list
        else:
            conducting_equipment = Conducting_equipment(equipment)
            conducting_equipment.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
            conducting_equipment.type = 'CE'
            # busbar section list
            if name == 'BusbarSection':
                busbar_section = Busbar_section(equipment)
                node_list.append(busbar_section)
                busbar_section.CE_type = 'Bus'
                busbar_section.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                busbar_section.equipmentcontainer_rdf_id = equipment.find('cim:Equipment.EquipmentContainer',ns).attrib.get(ns['rdf']+'resource')
                for voltagelevel in gridEQ.findall('cim:VoltageLevel',ns):
                    if voltagelevel.attrib.get(ns['rdf']+'ID') == busbar_section.equipmentcontainer_rdf_id.replace("#", "") :
                        basevoltage_id = voltagelevel.find('cim:VoltageLevel.BaseVoltage',ns).attrib.get(ns['rdf']+'resource')
                        for Basevoltage in gridEQ.findall('cim:BaseVoltage',ns):
                            if Basevoltage.attrib.get(ns['rdf']+'ID') == basevoltage_id.replace("#", "") :
                                busbar_section.basevoltage = float(Basevoltage.find('cim:BaseVoltage.nominalVoltage',ns).text)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                busbar_section_list.append(busbar_section)
           
            # energy consumer load list
            elif name == 'EnergyConsumer':
                energy_consumer_load = Energy_consumer_load(equipment)
                energy_consumer_load.CE_type = 'Load'
                energy_consumer_load.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                energy_consumer_load_list.append(energy_consumer_load)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                node_list.append(energy_consumer_load)
            
            # synchronous machine list
            elif name == 'SynchronousMachine':
                synchronous_machine = Synchronous_machine(equipment)
                synchronous_machine.CE_type = 'Generator'
                synchronous_machine.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                synchronous_machine_list.append(synchronous_machine)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                node_list.append(synchronous_machine)
            
            # AC line segment list
            elif name == 'ACLineSegment':
                AC_line_segment = AC_Line_segment(equipment)
                AC_line_segment.CE_type = 'Line'        
                AC_line_segment.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                AC_line_segment_list.append(AC_line_segment)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                node_list.append(AC_line_segment)
                
            # power transformer list
            elif name == 'PowerTransformer':
                power_transformer = Power_transformer(equipment)
                power_transformer.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                power_transformer.CE_type = 'Transformer'
                power_transformer_list.append(power_transformer)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                node_list.append(power_transformer)
            
            # breaker list
            elif name == 'Breaker':
                breaker = Breaker(equipment)
                breaker_list.append(breaker)
                breaker.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                breaker.CE_type = 'Breaker' 
                node_list.append(breaker)
                for state in gridSSH.findall('cim:Breaker',ns):
                    if state.attrib.get(ns['rdf']+'ID') == conducting_equipment.rdf_id:
                        breaker.BreakerOpen = state.find('cim:Switch.Open',ns).text 
            
            # linear shunt compensator list
            elif name == 'LinearShuntCompensator':
                linear_shunt_compensator = Linear_shunt_compensator(equipment)
                linear_shunt_compensator.CE_type = 'Compensator'
                linear_shunt_compensator.rdf_id = equipment.attrib.get(ns['rdf']+'ID')
                linear_shunt_compensator_list.append(linear_shunt_compensator)
                conducting_equipment.name = equipment.find('cim:IdentifiedObject.name',ns).text
                node_list.append(linear_shunt_compensator)


# testing part
# terminal index
print('Terminals:')
for TE in node_list:
    if TE.type == 'TE':
        print(node_list.index(TE))
        # the index are from 39 to 77
        
# connectivity node index
print('ConnectivityNodes:')
for CN in node_list:
    if CN.type == 'CN':
        print(node_list.index(CN))
        # the index are from 16 to 29
        
# conducting equipment index
print('Conducting Equipments:')
for CE in node_list:
    if CE.type == 'CE':
        print(node_list.index(CE))
        # the index are from 0 to 15 and from 30 to 38
        
# find the connectivity node which is attached to a terminal
for i in terminal_list:
    for j in node_list:
        if j.type == 'CN' and i.CN_rdf_id.replace("#", "") == j.rdf_id:
            j.Terminal_list.append(i)
            j.num_attachTerms = len(j.Terminal_list)


# find the conducting equipment which is attached to a terminal
for i in terminal_list:
    for j in node_list:
        if j.type == 'CE' and i.CE_rdf_id.replace("#", "") == j.rdf_id:
            j.Terminal_list.append(i)
            j.num_attachTerms = len(j.Terminal_list)

# find next node
def find_next_node(prev_node, curr_node):
    if curr_node.type == 'TE' and prev_node.type == 'CE':
        next_node_rdf_id = curr_node.CN_rdf_id
        for node in node_list:
            if next_node_rdf_id.replace('#','') == node.rdf_id:
                return(node)
    else:
        next_node_rdf_id = curr_node.CE_rdf_id
        for node in node_list:
            if next_node_rdf_id == '#' + node.rdf_id:
                return(node)
                                       
    if curr_node.type == 'CN':
        return(random.choice(curr_node.Terminal_list))
            
    elif curr_node.type == 'CE':    
        return(random.choice(curr_node.Terminal_list))

# traversal algorithm initialization
CN_CE_stack =[]
CN_CE_type_stack = []
stack_list = []
type_stack_list = []

# find connectivity node which is attatched to busbar
CN_attached_to_busbar_list = []
for i in node_list:
    for j in i.Terminal_list:
        if i.type == 'CN':
            prev_node = i
            curr_node = j
            next_node = find_next_node(prev_node, curr_node)
            if next_node.CE_type == 'Bus':
                CN_attached_to_busbar_list.append(i)
# print(CN_attached_to_busbar_list)

#list of CNs that are not attached to busbar
CN_not_attached_to_busbar_list = []
for i in connectivity_node_list:
    if i not in CN_attached_to_busbar_list:
        CN_not_attached_to_busbar_list.append(i)
# print(CN_not_attached_to_busbar_list)

# loop between CNs:
for i in connectivity_node_list:   
    if i.num_attachTerms > 0:
        for j in i.Terminal_list:
            if j.traversal_flag == 0:
                CN_CE_stack = [i]
                CN_CE_type_stack = [i.type]
                curr_node = i
                i.num_attachTerms -=1
                j.traversal_flag = 1
                prev_node = curr_node
                curr_node = j
                next_node = find_next_node(prev_node, curr_node)
                CN_CE_stack.append(next_node)
                CN_CE_type_stack.append(next_node.type)
                k = next_node
                if k.num_attachTerms > 1:
                    for l in k.Terminal_list:
                        if l.traversal_flag == 0:
                            l.traversal_flag =1 
                            prev_node = k
                            curr_node = l
                            next_node = find_next_node(prev_node, curr_node)
                            CN_CE_stack.append(next_node)
                            CN_CE_type_stack.append(next_node.type)
            if CN_CE_stack not in stack_list:
                stack_list.append(CN_CE_stack)
                type_stack_list.append(CN_CE_type_stack)

print('stack_list:')
print(stack_list) 
print(type_stack_list)

# pandapower
print('PandaPower:')
net = pp.create_empty_network()


# create bus
# conducting equipment__Bus
for i in busbar_section_list:
    i.bus = pp.create_bus(net, name= i.name, vn_kv = i.basevoltage, type='b')
# connectivity nodes which are not attached to busbar
for j in CN_not_attached_to_busbar_list:
    j.bus = pp.create_bus(net, name= j.name, vn_kv = j.basevoltage, type='n')
# connectivity nodes which are attached to busbar
for i in CN_attached_to_busbar_list:
    for j in i.Terminal_list:
            prev_node = i
            curr_node = j
            next_node = find_next_node(prev_node, curr_node)
            if next_node.CE_type == 'Bus':
                i.bus = next_node.bus
net.bus


# create transformer
pp_transformer_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Transformer':
            if i[0].basevoltage > i[-1].basevoltage:
                bus_hv = i[0].bus
                bus_lv = i[-1].bus
            else:
                bus_hv = i[-1].bus
                bus_lv = i[0].bus
            pp_transformer_list.append(pp.create_transformer(net, bus_hv, bus_lv, name = j.name, std_type = "25 MVA 110/20 kV"))
net.trafo
# print(pp_transformer_list)


# create lines
pp_line_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Line':
            pp_line_list.append(pp.create_line(net, i[0].bus, i[-1].bus, length_km = 2, std_type = "N2XS(FL)2Y 1x300 RM/35 64/110 kV",  name= j.name))

net.line
# print(pp_line_list)


# create switches
pp_breaker_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Breaker':
            if j.breakeropen == 'false':
                pp_breaker_list.append(pp.create_switch(net, i[0].bus, i[-1].bus, et="b", type="CB", closed=True))
            else:
                pp_breaker_list.append(pp.create_switch(net, i[0].bus, i[-1].bus, et="b", type="CB", closed=False))
net.switch
# print(pp_breaker_list)


# create generators
pp_generator_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Generator':
            pp_generator_list.append(pp.create_sgen(net, i[0].bus, p_mw=2, q_mvar=-0.6, name = j.name))        
net.sgen
# print(pp_generator_list)

# create load
pp_load_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Load':
            pp_load_list.append(pp.create_load(net, i[0].bus, p_mw=2, q_mvar=1, scaling=0.65, name = j.name))     
net.load
# print(pp_load_list)

# create shunt
pp_shunt_list = []
for i in stack_list:
    for j in i:
        if j.CE_type == 'Compensator':
            pp_shunt_list.append(pp.create_shunt(net, i[0].bus, q_mvar=-0.95, p_mw=0, name = j.name))
net.shunt
# print(pp_shunt_list)

print(net)
print(net.bus)
print(net.trafo)
print(net.line)
print(net.switch)
print(net.sgen)
print(net.load)
print(net.shunt)
pp.plotting.simple_plot(net)


for terminal in terminal_list:
    if terminal.traversal_flag == 0:
        print('There is still terminal untraversed.')