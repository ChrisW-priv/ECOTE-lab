using System;

public class Class1
{
    public string Name { get; set; }
    public Class1 Parent { get; set; }
    public Class1 Bestfriend { get; set; }

    public Class1(string name, Class1 parent, Class1 bestfriend)
    {
        Name = name;
        Parent = parent;
        Bestfriend = bestfriend;
    }

    public override bool Equals(object obj)
    {
        throw new NotImplementedException();
    }

    protected override void Finalize()
    {
        // Finalize resources if necessary
    }

    public override int GetHashCode()
    {
        throw new NotImplementedException();
    }

    protected object MemberwiseClone()
    {
        throw new NotImplementedException();
    }

    public override string ToString()
    {
        throw new NotImplementedException();
    }
}