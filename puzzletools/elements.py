from puzzletools.enumeration import EnumerationMeta

class ChemicalElement(metaclass=EnumerationMeta):

    fields = ['number','symbol','name']

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return '< Element %s >'%self
    
    data = [
        (1,'H','Hydrogen'),
        (2,'He','Helium'),
        (3,'Li','Lithium'),
        (4,'Be','Beryllium'),
        (5,'B','Boron'),
        (6,'C','Carbon'),
        (7,'N','Nitrogen'),
        (8,'O','Oxygen'),
        (9,'F','Fluorine'),
        (10,'Ne','Neon'),
        (11,'Na','Sodium'),
        (12,'Mg','Magnesium'),
        (13,'Al','Aluminum'),
        (14,'Si','Silicon'),
        (15,'P','Phosphorus'),
        (16,'S','Sulfur'),
        (17,'Cl','Chlorine'),
        (18,'Ar','Argon'),
        (19,'K','Potassium'),
        (20,'Ca','Calcium'),
        (21,'Sc','Scandium'),
        (22,'Ti','Titanium'),
        (23,'V','Vanadium'),
        (24,'Cr','Chromium'),
        (25,'Mn','Manganese'),
        (26,'Fe','Iron'),
        (27,'Co','Cobalt'),
        (28,'Ni','Nickel'),
        (29,'Cu','Copper'),
        (30,'Zn','Zinc'),
        (31,'Ga','Gallium'),
        (32,'Ge','Germanium'),
        (33,'As','Arsenic'),
        (34,'Se','Selenium'),
        (35,'Br','Bromine'),
        (36,'Kr','Krypton'),
        (37,'Rb','Rubidium'),
        (38,'Sr','Strontium'),
        (39,'Y','Yttrium'),
        (40,'Zr','Zirconium'),
        (41,'Nb','Niobium'),
        (42,'Mo','Molybdenum'),
        (43,'Tc','Technetium'),
        (44,'Ru','Ruthenium'),
        (45,'Rh','Rhodium'),
        (46,'Pd','Palladium'),
        (47,'Ag','Silver'),
        (48,'Cd','Cadmium'),
        (49,'In','Indium'),
        (50,'Sn','Tin'),
        (51,'Sb','Antimony'),
        (52,'Te','Tellurium'),
        (53,'I','Iodine'),
        (54,'Xe','Xenon'),
        (55,'Cs','Cesium'),
        (56,'Ba','Barium'),
        (57,'La','Lanthanum'),
        (58,'Ce','Cerium'),
        (59,'Pr','Praseodymium'),
        (60,'Nd','Neodymium'),
        (61,'Pm','Promethium'),
        (62,'Sm','Samarium'),
        (63,'Eu','Europium'),
        (64,'Gd','Gadolinium'),
        (65,'Tb','Terbium'),
        (66,'Dy','Dysprosium'),
        (67,'Ho','Holmium'),
        (68,'Er','Erbium'),
        (69,'Tm','Thulium'),
        (70,'Yb','Ytterbium'),
        (71,'Lu','Lutetium'),
        (72,'Hf','Hafnium'),
        (73,'Ta','Tantalum'),
        (74,'W','Tungsten'),
        (75,'Re','Rhenium'),
        (76,'Os','Osmium'),
        (77,'Ir','Iridium'),
        (78,'Pt','Platinum'),
        (79,'Au','Gold'),
        (80,'Hg','Mercury'),
        (81,'Tl','Thallium'),
        (82,'Pb','Lead'),
        (83,'Bi','Bismuth'),
        (84,'Po','Polonium'),
        (85,'At','Astatine'),
        (86,'Rn','Radon'),
        (87,'Fr','Francium'),
        (88,'Ra','Radium'),
        (89,'Ac','Actinium'),
        (90,'Th','Thorium'),
        (91,'Pa','Protactinium'),
        (92,'U','Uranium'),
        (93,'Np','Neptunium'),
        (94,'Pu','Plutonium'),
        (95,'Am','Americium'),
        (96,'Cm','Curium'),
        (97,'Bk','Berkelium'),
        (98,'Cf','Californium'),
        (99,'Es','Einsteinium'),
        (100,'Fm','Fermium'),
        (101,'Md','Mendelevium'),
        (102,'No','Nobelium'),
        (103,'Lr','Lawrencium'),
        (104,'Rf','Rutherfordium'),
        (105,'Db','Dubnium'),
        (106,'Sg','Seaborgium'),
        (107,'Bh','Bohrium'),
        (108,'Hs','Hassium'),
        (109,'Mt','Meitnerium'),
        (110,'Ds','Darmstadtium'),
        (111,'Rg','Roentgenium'),
        (112,'Cn','Copernicium'),
        (113,'Uut','Ununtrium'),
        (114,'Fl','Flerovium'),
        (115,'Uup','Ununpentium'),
        (116,'Lv','Livermorium'),
        (117,'Uuh','Ununseptium'),
        (118,'Uuo','Ununoctium'),
    ]

_short_symbols = { e.symbol for e in ChemicalElement.items if len(e.symbol)<=2 }

def parse_as_element_symbols(s):
    '''
    Given a string `s`, returns a tuple whose first element is the number of
    ways of parsing `s` as a sequence of element symbols, and whose second
    element is one such parsing (or `None` if none exists).

        >>> parse_as_element_symbols('the south')
        (1, ['Th', 'Es', 'O', 'U', 'Th'])
    '''
    s = ''.join(c for c in s if c.isalpha())
    c1 = 1
    p1 = []
    c2 = 0
    p2 = None
    partial = [(0,None),(1,[])]
    for i in range(len(s)):
        one = s[i].title()
        two = s[i-1:i+1].title()
        one_works = p1 is not None and one in _short_symbols
        two_works = p2 is not None and two in _short_symbols
        if two_works:
            p = p2 + [two]
        elif one_works:
            p = p1 + [one]
        else:
            p = None
        c = c1*one_works+c2*two_works
        c1, c2 = c, c1
        p1, p2 = p, p1
    return (c1,p1)
