using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

class Program
{
    static async Task Main(string[] args)
    {

        var ipAddresses = File.ReadAllLines("IPs.txt");

        var countryCount = new Dictionary<string, int>();

        using (var client = new HttpClient())
        {
            foreach (var ip in ipAddresses)
            {
                var response = await client.GetStringAsync($"https://ipinfo.io/{ip}/json");
                var ipData = JsonConvert.DeserializeObject<IpData>(response);

                if (ipData != null && !string.IsNullOrEmpty(ipData.Country))
                {
                    if (countryCount.ContainsKey(ipData.Country))
                    {
                        countryCount[ipData.Country]++;
                    }
                    else
                    {
                        countryCount[ipData.Country] = 1;
                    }
                }
            }
        }

        foreach (var kvp in countryCount)
        {
            Console.WriteLine($"{kvp.Key} - {kvp.Value}");
        }

        var maxCountry = countryCount.OrderByDescending(kvp => kvp.Value).FirstOrDefault();
        Console.WriteLine($"Страна с наибольшим количеством IP: {maxCountry.Key}");

        if (maxCountry.Key == "RU")
        {
            Console.WriteLine("Города России: Москва, Санкт-Петербург, Казань, Екатеринбург...");
        }
    }
}

public class IpData
{
    [JsonProperty("country")]
    public string Country { get; set; }
}
