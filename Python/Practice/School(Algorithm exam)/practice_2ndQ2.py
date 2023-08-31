def bubble(n, job):
    for i in range(n):
        for j in range(n-1):
            if(int(job[j]) > int(job[j+1])):
                temp = job[j]
                job[j] = job[j+1]
                job[j+1] = temp

                temp = jid[j]
                jid[j] = jid[j+1]
                jid[j + 1] = temp


def Schedule(c, job, n, jid):
    if c == 'A':
        return job.pop(0), jid.pop(0)

    if c == 'B':
        return job.pop(-1), jid.pop(-1)


if __name__ == '__main__':
    n = int(input())
    job = list(map(str, input().rstrip().split()))
    jid = []
    for i in range(n):
        jid.append(i+1)

    bubble(n, job)

    AWork = 0
    BWork = 0
    for i in range(n):
        if AWork > BWork:
            day, name = Schedule('B', job, n, jid)
            BWork = BWork + int(day)
            print("Team B 執行 job"+str(name)+" 需要 "+str(day)+" 天")

        elif AWork < BWork:
            day, name = Schedule('A', job, n, jid)
            AWork = AWork + int(day)
            print("Team A 執行 job"+str(name)+" 需要 "+str(day)+" 天")

        else:
            day, name = Schedule('A', job, n, jid)
            AWork = AWork + int(day)
            print("Team A 執行 job"+str(name)+" 需要 "+str(day)+" 天")
