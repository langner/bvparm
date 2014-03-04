import sys
import urllib


bvparm_cif = "bvparm2013.cif"
bvparm_cif_url = "http://www.iucr.org/__data/assets/file/0006/81087/bvparm2013.cif"

class BondValenceParameters:

    loop_references = ["_valence_ref_id", "_valence_ref_reference"]
    loop_parameters = [ "_valence_param_atom_1", "_valence_param_atom_1_valence",
                        "_valence_param_atom_2", "_valence_param_atom_2_valence",
                        "_valence_param_Ro", "_valence_param_B",
                        "_valence_param_ref_id", "_valence_param_details" ]
    loop_parameter_names = ["atom1", "valence1", "atom2", "valence2", "r0", "b", "ref", "details"]
    loop_parameter_types = [str, int, str, int, float, float, str, str]

    def __init__(self, source=None, fallback=[bvparm_cif, bvparm_cif_url]):
        self.source = source
        self.fallback = fallback
        self.__get_cif()
        self.__parse_cif()

    def __get_cif(self):
        if self.source:
            f = urllib.urlopen(self.source)
            print "Reading parameters from %s" % self.source
        else:
            for source in self.fallback:
                try:
                    f = urllib.urlopen(source)
                    self.source = source
                    print "Reading parameters from %s" % source
                    break
                except:
                    print "Could not open %s" % source
        self.cif = f.read()

    def __parse_cif(self):
        self.cif_lines = self.cif.split("\n")
        for il, line in enumerate(self.cif_lines):
            if line.strip() == "loop_":
                next = []
                for i in range(1,3):
                    next.append(self.cif_lines[il+i].strip())
                if next == self.loop_references:
                    self.__extract_references(il+3, self.cif_lines[il+3])
                    continue
                for i in range(3,9):
                    next.append(self.cif_lines[il+i].strip())
                if next == self.loop_parameters:
                    self.__extract_parameters(il+9, self.cif_lines[il+9])
                

    def __extract_references(self, il, line):
        self.references = {}
        while not self.cif_lines[il].strip():
            il += 1
        while self.cif_lines[il].strip():
            line = self.cif_lines[il]
            lbl = line.split()[0]
            ref = " ".join(line.split()[1:])
            self.references[lbl] = ref
            il += 1

    def __extract_parameters(self, il, line):

        while not self.cif_lines[il].strip():
            il += 1

        self.parameters = {}
        while self.cif_lines[il].strip() and not "EOF" in self.cif_lines[il]:

            line = self.cif_lines[il]
            columns = line.split()

            names = self.loop_parameter_names
            types = self.loop_parameter_types
            if len(columns) == 8:
                data = dict([(lbl,types[i](columns[i])) for i,lbl in enumerate(names)])
            else:
                data = dict([(lbl,types[i](columns[i])) for i,lbl in enumerate(names[:-1])])
                data['details'] = line[line.index(columns[7]):]

            if not data['atom1'] in self.parameters:
                self.parameters[data['atom1']] = {}
            cation = self.parameters[data['atom1']]

            if not data['valence1'] in cation:
                cation[data['valence1']] = {}
            cvalence = cation[data['valence1']]

            if not data['atom2'] in cvalence:
                cvalence[data['atom2']] = {}
            anion = cvalence[data['atom2']]

            if not data['valence2'] in anion:
                anion[data['valence2']] = []
            anion[data['valence2']].append({})
            avalence = anion[data['valence2']][-1]

            avalence['r0'] = data['r0']
            avalence['b'] = data['b']
            avalence['ref'] = data['ref']
            avalence['details'] = data['details']    
       
            il += 1

    def __getitem__(self, cation):
        return self.parameters[cation]


if __name__ == '__main__':
    params = BondValenceParameters(*(sys.argv[1:]))
    anions_K = sorted(params.parameters['K'][1].keys())
    print "BV parameters available for K bonded to: " + ", ".join(anions_K)
