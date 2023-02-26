import os
import re
import time

pattern_pc=r'[A-Z]+(_.+?\|.+?\|turn\d+)? (G=\d+ )?\d+ \d+ \d \d+\n'
pattern_pc+=r'(WISH \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+\n)?'
pattern_pc+=r'(AMULET ([A-Z]+ \d+ )+ENDAMULET\n)?'
pattern_pc+=r'\d+ \d+ \d+ \d+ \d+ \d+ ?\n'
pattern_pc+=r'([A-Z]+ \d+ \d+ \d+ \d+ \d+ \d|NONE)\n'*4
pattern_pc+=r'\d( [A-Z]+)*'

class GEAR:
    def __init__(self,string):
        pattern=r'(([A-Z]+) (\d+ \d+ \d+ \d+ \d+) (\d)|NONE)'
        match=re.search(pattern,string).groups()
        self.string=match[0]
        self.type=match[1]
        self.attribute=match[2]
        if match[3]:
            self.myst=bool(int(match[3]))
        else:
            self.myst=match[3]

    def __str__(self):
        return self.string
    
    def transform(self):
        '''将神秘装备的名称导出'''
        if self.myst:
            return 'M_'+self.type
        else:
            return self.type

class PC:
    def __init__(self,string):
        pattern=r'(?P<string>'
        pattern+=r'(?P<role>[A-Z]+)_(?P<name>(?P<group>.+?)\|(?P<mode>.+?)\|turn(?P<turn>\d+)) (?P<growth>G=\d+ )?(?P<card>\d+ \d+ \d \d+)\n'
        pattern+=r'(?:WISH (?P<wish>\d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+)\n)?'
        pattern+=r'(?:AMULET (?P<amulet>(?:[A-Z]+ \d+ )+)ENDAMULET\n)?'
        pattern+=r'(?P<attribute>\d+ \d+ \d+ \d+ \d+ \d+) ?\n'
        pattern+=r'(?P<weapon>[A-Z]+ \d+ \d+ \d+ \d+ \d+ \d|NONE)\n'
        pattern+=r'(?P<hand>[A-Z]+ \d+ \d+ \d+ \d+ \d+ \d|NONE)\n'
        pattern+=r'(?P<body>[A-Z]+ \d+ \d+ \d+ \d+ \d+ \d|NONE)\n'
        pattern+=r'(?P<head>[A-Z]+ \d+ \d+ \d+ \d+ \d+ \d|NONE)\n'
        pattern+=r'(?P<aura>\d(?: [A-Z]+)*)'+r')'
        match=re.search(pattern,string)
        self.string=match['string']
        self.role=match['role']
        self.name=match['name']
        self.group=match['group']
        self.mode=match['mode']
        self.turn=match['turn']
        self.growth=match['growth']
        self.card=match['card']
        self.wish=match['wish']
        self.amulet=match['amulet']
        self.attribute=match['attribute']
        self.weapon=GEAR(match['weapon'])
        self.hand=GEAR(match['hand'])
        self.body=GEAR(match['body'])
        self.head=GEAR(match['head'])
        self.aura=match['aura']        

    def __str__(self):
        return self.string
    
    def __eq__(self,other):
        return (self.role,self.name)==(other.role,other.name)
    
    def __hash__(self):
        return hash((self.role,self.name))

def read_lib():
    '''读取lib.txt，返回包含信息的字典'''
    with open('代码\\lib.txt',mode='r',encoding='UTF-8') as f:
        lib=f.read()

    pattern=r'\[(.+?)\]([^\[\]]+)'
    match=re.findall(pattern,lib,flags=re.S)
    dt=dict(map(lambda t:(t[0],tuple(t[1].split())),match))
    return dt

def read_option():
    '''读取option.txt，返回包含信息的字典'''
    with open('option.txt',mode='r',encoding='UTF-8') as f:
        option=f.read()
    
    def read_info(info):
        '''读取信息，以给定的形式返回'''
        def read_info1(info):
            '''读取形如a=x b=y的信息，返回包含信息的字典'''
            return dict(re.findall(r'(.+)=(.+)',info))
        
        def read_info2(info):
            '''读取形如a={} b={}的信息，返回包含信息的字典'''
            match=re.findall(r'(.+)={(.+)}',info)
            dt=dict(map(lambda t:(t[0],tuple(map(lambda s:tuple(s.split(' ')),t[1].split(';')))),match))
            return dt

        def read_info3(info):
            '''读取形如{a=x b=y} {c=z d=w}的信息，返回包含信息的字典组成的元组'''
            match=re.findall(r'{(.+?)}',info,flags=re.S)
            dt=tuple(map(lambda t:dict(re.findall(r'(.+)=(.*)',t)),match))
            return dt
        
        if(not re.search(r'[{}]',info)):
            return read_info1(info)
        elif(re.search(r'={.+}',info)):
            return read_info2(info)
        elif(re.search(r'{[^{}]*=[^{}]*}',info)):
            return read_info3(info)

    pattern=r'\[(.+?)\]([^\[\]]+)'
    match=re.findall(pattern,option,flags=re.S)
    dt=dict(map(lambda t:(t[0],read_info(t[1])),match)) #返回字典，value为option中key对应的信息
    return dt

def mode(defender):
    '''将defender转化为mode'''
    if(defender=='0'):
        return 'ATK'
    elif(defender=='1'):
        return 'DEF'
    elif(defender=='2'):
        return 'MIX'

def initialize(groups):
    '''若首次进行迭代，则对'记录'文件夹进行初始化'''
    try:
        os.mkdir('记录')
    except:
        pass
    
    if not os.listdir('记录'):
        with open('记录\\turn0.txt',mode='w+',encoding='UTF-8') as f:
            for group in groups:
                f.write(f'MIN_{group["Name"]}|{mode(group["Defender"])}|turn0 {group["Card"]}\n')
                f.write(f'{int(int(group["Card"].split()[0])/2)} '*6+'\n')
                f.write(f'SHIELD {group["Gear"]}\n')
                f.write(f'GLOVES {group["Gear"]}\n')
                f.write(f'THORN {group["Gear"]}\n')
                f.write(f'TIARA {group["Gear"]}\n')
                f.write('4 SHENG SHANG CI JUE\n\n')

def get_turn():
    '''返回当前轮数'''
    return max(map(lambda s:int(re.search(r'\d+',s).group()),os.listdir('记录')))

def read_pool():
    '''读取算点对手PC，返回字典，分别由总池子、ATK池子、DEF池子、MIX池子的列表构成'''
    initialize(tuple(group for group in read_option()['Group']))
    
    with open(f'记录\\turn{get_turn()}.txt',mode='r',encoding='UTF-8') as f:
        pool_all=list(map(lambda s:PC(s.group()),re.finditer(pattern_pc,f.read())))
    
    dt={'ALL':pool_all}
    for m in ('ATK','DEF','MIX'):
        dt[m]=[pc for pc in pool_all if pc.mode==m]
    return dt

def calculate():
    '''调用newkf_64.exe进行算点，结果输出至output.txt'''
    cmd='cd 代码 & newkf_64.exe < input.txt > output.txt'
    os.system(cmd)

def write_newkf_apc(group,role):
    '''将当前group和当前role的PC信息写入newkf.in'''
    with open('代码\\newkf_sample.in',mode='r',encoding='UTF-8') as f:
        sample=f.read()
    
    sample=sample.replace('<Aura_value>',group['Aura value'],1)
    sample=sample.replace('<Role>',role,1)

    if role in read_lib()['Growth'] and group['Growth']:
        sample=sample.replace('<Growth>','G='+group['Growth'],1)
    else:
        sample=sample.replace('<Growth> ','',1)

    sample=sample.replace('<Card>',group['Card'],1)

    if group['Wish']:
        sample=sample.replace('<Wish>','WISH '+group['Wish'],1)
    else:
        sample=sample.replace('<Wish>\n','',1)

    if group['Amulet']:
        sample=sample.replace('<Amulet>','AMULET '+group['Amulet']+' ENDAMULET',1)
    else:
        sample=sample.replace('<Amulet>\n','',1)
    
    if group['Defender']=='0':
        enemy=read_pool()['DEF']+read_pool()['MIX']
    elif group['Defender']=='1':
        enemy=read_pool()['ATK']+read_pool()['MIX']
    elif group['Defender']=='2':
        enemy=read_pool()['ALL']
    sample=sample.replace('<Enemy>','\n\n'.join(map(lambda pc:pc.string,enemy)),1)

    gear_string=''
    if(group['Gear']):
        for gear in read_lib()['Gear']:
            if int(read_option()['Gear'][gear]) and gear not in read_option()['Role'][role][0]:
                gear_string+=f'{gear} {group["Gear"]}\n'
    if(group['Myst']):
        for myst in read_lib()['Myst']:
            if int(read_option()['Myst'][myst]) and myst not in read_option()['Role'][role][1]:
                gear_string+=f'{myst} {group["Myst"]}\n'
    sample=sample.replace('<Gear>\n',gear_string,1)

    sample=sample.replace('<Threads>',read_option()['Calculation']['Threads'],1)
    sample=sample.replace('<Tests>',read_option()['Calculation']['Tests'],1)
    sample=sample.replace('<Seedmax>',read_option()['Calculation']['Seedmax'],1)

    aura_string='_'.join(aura for aura in read_lib()['Aura']
        if not int(read_option()['Aura'][aura]) or aura in read_option()['Role'][role][2])
    if aura_string:
        sample=sample.replace('<Aura_filter>',aura_string,1)
    else:
        sample=sample.replace('AURAFILTER <Aura_filter>\n','',1)

    sample=sample.replace('<Defender>',group['Defender'],1)
    sample=sample.replace('<Verbose>',read_option()['Calculation']['Verbose'],1)

    with open('代码\\newkf.in',mode='w+',encoding='UTF-8') as f:
        f.write(sample)

def read_rezult_apc():
    '''读取output.txt，返回PC算点结果和胜率的元组'''
    with open('代码\\output.txt',mode='r',encoding='UTF-8') as f:
        output=f.read()

    pc_string=re.search(pattern_pc,output).group()
    
    win_rate=float(re.search('Average Win Rate : ([\d\.]+)%',output).group(1))
    return pc_string,win_rate

def apc(group,role):
    '''对当前group和当前role进行apc算点，返回胜率和PC算点结果的元组'''
    with open('代码\\input.txt',mode='w+',encoding='UTF-8') as f:
        f.write('apc\nq')

    write_newkf_apc(group,role)
    calculate()

    rezult=read_rezult_apc()
    return rezult

def write_newkf_vb(pool_all):
    '''将PC池子写入newkf.in'''
    with open('代码\\newkf_sample.in',mode='r',encoding='UTF-8') as f:
        sample=f.read()
    
    sample=sample.replace('<Aura_value>','0',1)
    sample=sample.replace('<Role> <Growth> <Card>\n<Wish>\n<Amulet>','LIN 700 500 4 8',1)
    sample=sample.replace('<Enemy>','\n\n'.join(map(lambda pc:pc.string,pool_all)),1)
    sample=sample.replace('<Gear>\n','',1)
    sample=sample.replace('<Threads>',read_option()['Calculation']['Threads'],1)
    sample=sample.replace('<Tests>',read_option()['Calculation']['Tests_vb'],1)
    sample=sample.replace('<Seedmax>',read_option()['Calculation']['Seedmax'],1)
    sample=sample.replace('AURAFILTER <Aura_filter>\n','',1)
    sample=sample.replace('<Defender>','2',1)
    sample=sample.replace('<Verbose>',read_option()['Calculation']['Verbose'],1)

    with open('代码\\newkf.in',mode='w+',encoding='UTF-8') as f:
        f.write(sample)

def read_rezult_vb():
    '''读取output.txt，返回胜率'''
    with open('代码\\output.txt',mode='r',encoding='UTF-8') as f:
        output=f.read()
    
    rezult=re.search('Win Rate : [\d\.]+% \((\d+)/(\d+) D=\d+\([\d\.]+%\)\)',output)
    return (int(rezult.group(1)),int(rezult.group(2)))

def vb(pool):
    '''对pool内的PC两两之间进行vb算点，返回key为(pc_ATK,pc_DEF)，value为胜率的字典'''
    write_newkf_vb(pool['ALL'])

    dt={}
    for pc_ATK in pool['ATK']+pool['MIX']:
        for pc_DEF in pool['DEF']+pool['MIX']:
            with open('代码\\input.txt',mode='w+',encoding='UTF-8') as f:
                f.write(f'vb PC {pc_ATK.name} PC {pc_DEF.name}\nq')
            
            calculate()
            dt[(pc_ATK,pc_DEF)]=read_rezult_vb()
    
    return dt

def sum_win_rate(dt,pool,pc):
    '''计算pc对pool中相应对手的胜率和，返回平均胜率'''
    try:
        win_rate=sum(map(lambda e:dt[(pc,e)][0],pool['ALL']))/sum(map(lambda e:dt[(pc,e)][1],pool['ALL']))
    except:
        win_rate=0.5
    return win_rate
    '''
    if(pc.mode=='ATK'):
        return sum(map(lambda e:dt[(pc,e)],pool['DEF']+pool['MIX']))/sum(map(lambda e:dt[(pc,e)],pool['DEF']+pool['MIX']))
    elif(pc.mode=='DEF'):
        return sum(map(lambda e:(100-dt[(e,pc)]),pool['ATK']+pool['MIX']))
    elif(pc.mode=='MIX'):
        return sum(map(lambda e:dt[(pc,e)],pool['DEF']+pool['MIX']))+sum(map(lambda e:(100-dt[(e,pc)]),pool['ATK']+pool['MIX']))
        '''

def iterate_group(group):
    '''对当前group和所有role进行apc算点，返回最高胜率的PC'''
    results=[apc(group,role) for role in read_lib()['Role']]
    results.sort(key=lambda t:-t[1])
    pc_string=results[0][0]
    match=re.search(pattern_pc,pc_string).group()
    
    return PC(match.replace(' ',f'_{group["Name"]}|{mode(group["Defender"])}|turn{get_turn()+1} ',1))

def iterate_turn():
    '''对所有group进行算点，将所得PC加入池子，两两之间进行vb算点，然后每组淘汰掉胜率最低的PC，所得池子写入txt'''
    pool=read_pool()
    for group in read_option()['Group']:
        pc_new=iterate_group(group)
        pool['ALL'].append(pc_new)
        pool[pc_new.mode].append(pc_new)

    dt=vb(pool)
    with open(f'记录\\turn{get_turn()+1}.txt',mode='w+',encoding='UTF-8') as f:
        for group in read_option()['Group']:
            lt=[pc for pc in pool[mode(group['Defender'])] if pc.group==group['Name']]
            lt.sort(key=lambda pc:-sum_win_rate(dt,pool,pc))
            if(len(lt)>int(group['Size'])):
                lt=lt[:int(group['Size'])]
            for pc in lt:
                f.write(pc.string+'\n\n')
            del lt

def main():
    for i in range(int(read_option()['Iteration']['Turns'])):
        start_time=time.time()
        iterate_turn()
        end_time=time.time()
        print(f'已完成第 {get_turn()} 轮迭代，用时 {end_time-start_time} s！')

try:
    start_time=time.time()
    main()
    end_time=time.time()
    print(f'Use time: {end_time-start_time} s')
    input()
except Exception as e:
    print(e)
    input()
