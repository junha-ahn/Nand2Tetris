class SymbolTable:
    CLASS_IDENTI = {
        'STATIC':'static',
        'FIELD':'field'
    }

    SUBROUTIN_IDENTI = {
        'ARG':'arg',
        'VAR':'var'
    }

    KIND = {
        'STATIC':'static',
        'FIELD':'field',
        'ARG':'arg',
        'VAR':'var'
    }


    def __init__(self):
        self.ifCounter = 0
        self.whileCounter = 0
        self.classSymbols = {
            'name': [],
            'type': [],
            'kind': [],
            'index': [],
        }

        self.subroutineSymbols = {
            'name': [],
            'type': [],
            'kind': [],
            'index': [],

        }

        self.indices = {
            self.CLASS_IDENTI['STATIC']: 0,
            self.CLASS_IDENTI['FIELD']: 0,
            self.SUBROUTIN_IDENTI['ARG']: 0,
            self.SUBROUTIN_IDENTI['VAR']: 0
        }


    def getSegmentByKind(self, kind):
        if kind == 'field': return 'this'
        if kind == 'static': return 'static'
        if kind == 'var': return 'local'
        if kind == 'arg': return 'argument'
        return 'none'

    def startSubroutine(self):
        self.subroutineSymbols = {
            'name': [],
            'type': [],
            'kind': [],
            'index': [],
        }

        self.indices['arg'] = 0
        self.indices['var'] = 0


    def Define(self, name, type, kind):
        if kind in ['static','field']:
            self.classSymbols.get('name').append(name)
            self.classSymbols.get('type').append(type)
            self.classSymbols.get('kind').append(kind)
            self.classSymbols.get('index').append(
                self.classSymbols.get('kind').count(kind) - 1
            )
            self.indices[kind] += 1
        
        elif kind in ['arg','var']:
            self.subroutineSymbols.get('name').append(name)
            self.subroutineSymbols.get('type').append(type)
            self.subroutineSymbols.get('kind').append(kind)
            self.subroutineSymbols.get('index').append(
                self.subroutineSymbols.get('kind').count(kind) - 1
            )
            self.indices[kind] += 1

    def VarCount(self, kind):
        return self.indices[kind]


    def KindOf(self, name):
        if self._lookup(name) == None:
            return None 

        range,index = self._lookup(name)
        return range.get('kind')[index]
        

    def TypeOf(self,name):
        if self._lookup(name) == None:
            return None 

        range,index = self._lookup(name)
        return range.get('type')[index]

    def IndexOf(self, name):
        if self._lookup(name) == None: return None 
        range,index = self._lookup(name)
        return range.get('index')[index]


    def _lookup(self, name):
        if name in self.classSymbols.get('name') != None:
            idx = self.classSymbols.get('name').index(name)
            return (self.classSymbols, idx)
        
        if name in self.subroutineSymbols.get('name') != None:
            idx = self.subroutineSymbols.get('name').index(name)
            return (self.subroutineSymbols, idx)
        
        return None