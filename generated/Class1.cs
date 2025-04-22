using System;

public class Class1
{
    public Class1 Parent { get; set; }
    public string Name { get; set; }

    public Class1(Class1 parent, string name)
    {
        Parent = parent;
        Name = name;
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