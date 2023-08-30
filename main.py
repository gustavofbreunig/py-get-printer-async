import netaddr
import asyncio
import aiosnmp

async def get_counter(ip):
    async with aiosnmp.Snmp(host=ip, port=161, community="public") as snmp:
        try:
            for res in await snmp.get(".1.3.6.1.2.1.25.3.2.1.3.1"):      
                return res                          
        except:
            pass

async def queue_tasks(ips):
    tasks = []
    for ip in ips:
        tasks.append(loop.create_task(get_counter(ip)))
    done, pending = await asyncio.wait(tasks)
    return done
    

if __name__ == "__main__":
    network = netaddr.IPNetwork("10.1.1.0/23")
    ignore = [str(network.network), str(network.broadcast)]
    ips = list(filter(lambda y: y not in ignore, map(lambda x: str(x), netaddr.IPSet([network])))) 

    loop = asyncio.get_event_loop()
    futures_return = loop.run_until_complete(queue_tasks(ips))
    loop.close()

    for future in futures_return:
        ret = future.result()
        if ret != None:
            print(f'Encontrado {ret.value}')
    