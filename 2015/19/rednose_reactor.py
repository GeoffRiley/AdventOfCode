from collections import defaultdict

rules = defaultdict(list)
rev_rules = defaultdict(list)

with open('input') as f:
    rep_text = f.read().splitlines(keepends=False)

calibration_molecule = rep_text[-1]
rep_text = rep_text[:-1]
for line in rep_text:
    if len(line.strip()) > 0:
        k, v = line.split(' => ')
        rules[k].append(v)
        rev_rules[v].append(k)

products = set()

for n in range(len(calibration_molecule)):
    a, b = calibration_molecule[:n], calibration_molecule[n:]
    for key, rep in rules.items():
        if b.startswith(key):
            c = b[len(key):]
            for r in rep:
                products.add(f'{a}{r}{c}')

print(f'Part 1: {len(products)}')
# Part 1: 576

total_elements = sum(1 for c in calibration_molecule if c.isupper())
total_open_brackets = calibration_molecule.count('Rn')
total_close_brackets = calibration_molecule.count('Ar')
total_commas = calibration_molecule.count('Y')

print(f'Part 2: {total_elements - total_open_brackets - total_close_brackets - total_commas * 2 - 1}')

'''
Al => ThF       ThF        A => RF        
Al => ThRnFAr   Th(F)      A => R(F)    
B => BCa        BCa        B => BD      
B => TiB        TiB        B => TB      
B => TiRnFAr    Ti(F)      B => T(F)    
Ca => CaCa      CaCa       D => DD     
Ca => PB        PB         D => PB       
Ca => PRnFAr    P(F)       D => P(F)     
Ca => SiRnFYFAr Si(F,F)    D => S(F,F)  
Ca => SiRnMgAr  Si(Mg)     D => S(M)   
Ca => SiTh      SiTh       D => SR     
F => CaF        CaF        F => DF      
F => PMg        PMg        F => PM      
F => SiAl       SiAl       F => SA     
H => CRnAlAr    C(Al)      H => C(A)    
H => CRnFYFYFAr C(F,F,F)   H => C(F,F,F) 
H => CRnFYMgAr  C(F,Mg)    H => C(F,M)  
H => CRnMgYFAr  C(Mg,F)    H => C(M,F)  
H => HCa        HCa        H => HD      
H => NRnFYFAr   N(F,F)     H => N(F,F)   
H => NRnMgAr    N(Mg)      H => N(M)    
H => NTh        NTh        H => NR      
H => OB         OB         H => OB       
H => ORnFAr     O(F)       H => O(F)     
Mg => BF        BF         M => BF       
Mg => TiMg      TiMg       M => TM     
N => CRnFAr     C(F)       N => C(F)     
N => HSi        HSi        N => HS      
O => CRnFYFAr   C(F,F)     O => C(F,F)   
O => CRnMgAr    C(Mg)      O => C(M)    
O => HP         HP         O => HP       
O => NRnFAr     N(F)       O => N(F)     
O => OTi        OTi        O => OT      
P => CaP        CaP        P => DP      
P => PTi        PTi        P => PT      
P => SiRnFAr    Si(F)      P => S(F)    
Si => CaSi      CaSi       S => DS     
Th => ThCa      ThCa       R => RD    
Ti => BP        BP         T => BP       
Ti => TiTi      TiTi       T => TT     
e => HF         HF         e => HF       
e => NAl        NAl        e => NA      
e => OMg        OMg        e => OM      

ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF
O(PBPM)DDDSRDDSRDDPBS(F)(F)DDSRDDSRDDDDDDS(F,F)S(M)DS(PTTBF,PBF(S)DS(T(F)SA)PTBPT(DSA)DPTTBPM,F)PT(F)S(DDF)(DF)DS(S(M)F,DS(M)DDSRP(F)PBDS(M)DDSRDS(TM)F)SRSRDDS(M)DDS(F)TBPT(DSA)DPT(F)PBPBDDSRDPBSRP(F)SRDSRDSRDPTBS(F,F)DDP(F)PBDDPBS(T(F)DP(F)S(DDDSRD(DF),DS(F)BDDDSRF)PBF)DS(F)(DDDF)S(F)T(PM)F

'''
