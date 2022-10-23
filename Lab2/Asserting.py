from symtable import Symbol

from SymbolTable import SymbolTable


def Assert():
    st=SymbolTable(105)
    assert st.get(1)=="No record found"

    st.add(1,"first add")
    st.add(109,"second add")
    st.add(3,2)
    st.add("stringkey",1)
    st.add("string1","string2")

    print("First look on st:"+str(st))

    assert st.get(1) == "first add"
    assert st.get(109) == "second add"
    assert st.get(3)==2
    assert st.get("stringkey") == 1
    assert st.get("string1") == "string2"

    st.delete(109)
    assert st.get(109) == "No record found"

    st.delete("string1")
    assert st.get("string1") == "No record found"
    
    print("Second look on st:"+str(st))

Assert()





