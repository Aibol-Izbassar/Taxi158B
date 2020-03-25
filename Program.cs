using System;

namespace Taxi158B
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = Convert.ToInt32(Console.ReadLine());
            int[] array;
            int taxiCount = 0;
            int[] StudGroup = {0, 0, 0, 0, 0};

            string[] nums_strings = Console.ReadLine().Split();
            array = new int[n];
            for (int i = 0; i < n; i++)
                array[i] = Convert.ToInt32(nums_strings[i]);

            for (int i = 0; i < array.Length; i++)
            {
                StudGroup[array[i]]++;
            }

            taxiCount += StudGroup[4];
            taxiCount += StudGroup[3];
            StudGroup[1] = StudGroup[1] - StudGroup[3];
            StudGroup[1] = StudGroup[1] < 0 ? 0 : StudGroup[1];

            taxiCount += StudGroup[2] / 2 + StudGroup[2] % 2;
            StudGroup[2] = StudGroup[2] % 2;
            StudGroup[1] = StudGroup[1] - 2 * StudGroup[2];
            if (StudGroup[1] > 0)
            {
                taxiCount += StudGroup[1] / 4;

                if (StudGroup[1] % 4 > 0) 
                {
                    taxiCount++;
                }
            }

            Console.WriteLine(taxiCount);
        }
    }
}
