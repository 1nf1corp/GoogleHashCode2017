import numpy as np
class PizzaSlicer(object):

    """Docstring."""

    def __init__(self):
        """

        """

    def __str__(self):
        return "\n".join(self.pizza)
        
    def get_data(self, filename):
        """Choices : small, medium, big, example"""
        with open('data/%s.in' %filename) as infile:
            return map(str.split,infile)

    def main(self,args):
        data = self.get_data(args.file)
        nrows,ncols,min_ing,maxtot = map(int,data[0]) 
        self.pizza = map(lambda x:x[0], data[1:])

        self.array = np.zeros((nrows,ncols))
        for i in range(nrows):
            for j in range(ncols):
                self.array[i,j] = 1 if self.pizza[i][j] == 'T' else -1

        self.nrows = nrows; self.ncols = ncols
        self.min_ing = min_ing; self.maxtot = maxtot
        
        if args.verbose:
            print "Number of rows   : ", nrows
            print "Number of columns: ", ncols
            print "Minimum of each ingredient: ", min_ing
            print "Max size per slice: ", maxtot
        else:
            print data[0]

        if args.prnt:
            print "This is our pizza:\n", self

        self.legals = self.legal_slices()
        print self.sort_slices(self.legals)
        self.test_slicer(args)

    def test_slicer(self,args):
        di,dj = self.legals[0]
        i = 0; j = 0

        self.array[i:i+di,j:j+dj]=0
        s = 0

        print np.all(self.array[i:i+di,j:j+dj])

        for x in range(self.nrows):
            for y in range(self.ncols):
                if self.array[x,y]!=0:
                    for dx, dy in self.legals:
                        if dx + x > self.nrows or dy+y >self.ncols:
                            continue
                        s = self.array[x:x+dx,y:y+dy]
                        min_ing = dx*dy - np.abs(np.sum(s))
                        if args.verbose:
                            print 'slice? | (%dx%d) | x=%d | y=%d | min ing:%d'%(dx, dy, x,
                                y,min_ing)
                        # np.abs(np.sum(s)) > total per 
                        if np.all(s) and np.abs(np.sum(s))<=(dx*dy-self.min_ing):
                            self.array[x:x+dx,y:y+dy] = 0
                            if args.verbose:
                                print self.array
                            if args.slow:
                                raw_input()
                            break
                        if args.slow:
                            raw_input()
        pdict = {1:'T',-1:'M',0:'.'}
        new_pizza = map(''.join, np.vectorize(lambda x: pdict[x])(self.array))

        print "Final pizza:\n", '\n'.join(new_pizza)
        M = self.ncols*self.nrows
        faults = np.sum(np.abs(self.array))
        print "Final score: %d of %d = %.2f %%" %(M-faults, M,
                100*(M-faults)/float(M))


    def legal_slices(self):
        """Returns legal slices. Must have area between min_ing and maxtot"""
        ls = []
        for i in range(1,self.maxtot+1):
            for j in range(1,self.maxtot/i+1):
                if i*j >= 2*self.min_ing and i*j <= self.maxtot:
                    #last check is redundant
                    ls.append([i,j])
        return ls
        
    def sort_slices(self, slices):
        """Sort slices by area and then by width"""
        return sorted(slices, key=lambda x:(x[0]*x[1], -x[0]-x[1]))



class Slice(object):
    def __init__(self,coords,size, ingr):
        self.coords  = coords
        self.size = size
        self.ingr = ingr



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',default='example')
    parser.add_argument('-v','--verbose',action='store_true',
                        default=False)
    parser.add_argument('-p','--prnt',action='store_true',
                        default=False)
    parser.add_argument('-s','--slow',action='store_true',
                        default=False)

    args = parser.parse_args()
    ps = PizzaSlicer()
    ps.main(args)

