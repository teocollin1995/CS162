import std.stdio;
import std.math;
import std.conv;

bool primetest(float val)
{

  if (val % 2 == 0){ return false; }
  else
  {
        float cur  = 3.0;
        while(cur <= (sqrt(val)))
        {
                if (val % cur == 0)
                {
                        return false;
                }

                        cur+=2;


        }
        return true;
  }



}

void main(string[] args)
{
        auto input = to!float(args[1]);

        float cur = 1;
        float curt = 1;
        while (cur < input)
        {
                curt +=2;
                if (primetest(curt))
                   {
                        cur++;
                   }

        }
        writeln("The ", input,"th prime is ", curt);

}
