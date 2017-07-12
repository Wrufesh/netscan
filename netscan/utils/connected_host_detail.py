import subprocess


class Netscan:
    def parser(self, *cmd):
        try:
            self.output = subprocess.check_output(cmd)
        except:
            return """"
                Check your command once again.
                The required program may not exist.
                Or you are not a superuser
                This program needs root privilege.
                """
        self.decoded_output = self.output.decode(encoding='UTF-8', errors='strict')
        self.str = self.decoded_output[0]
        self.c = 0
        self.data_list = []
        for i in range(1, len(self.decoded_output)):
            if self.decoded_output[i] == ' ':
                if self.str != '':
                    self.data_list.append(self.str)
                self.c = self.c + 1
                self.str = ''
            elif self.decoded_output[i:i + 1] == "\n":
                if self.str != '':
                    self.data_list.append(self.str)
                self.str = ''
                self.data_list.append("\n")
                i = i + 1
            else:
                if self.c != 0:
                    self.data_list.append(self.c)
                self.str = self.str + self.decoded_output[i]
                self.c = 0
        return self.data_list

    def getIpMask(self, lyst):
        self.inb_list = []
        temp = ''
        binary = ''
        subnet = 0
        for j in range(10, len(lyst)):
            # self.print(lyst[j-10])
            if lyst[j - 2] == 'broadcast' and lyst[j - 6] == 'netmask' and lyst[j - 10] == 'inet':
                self.inb_list.append(lyst[j - 8])
                self.inb_list.append(lyst[j - 4])
                self.inb_list.append(lyst[j])
        # print(self.inb_list)
        # Checking for the connection
        if len(self.inb_list) == 0:
            return (False, "Not connected_hosts.html to the internet")
        # Extracting address in ip/mask form and returning it
        self.netmask = self.inb_list[1]
        for k in range(0, len(self.netmask)):
            if self.netmask[k] != '.':
                temp = temp + self.netmask[k]
            else:
                binary = binary + bin(int(temp))
                temp = ''
        binary = binary + bin(int(temp))
        for l in range(0, len(binary)):
            if binary[l] == '1':
                subnet = subnet + 1
        self.ip_mask = self.inb_list[0] + "/" + str(subnet)
        return (True, self.ip_mask)

    def scanResult(self, list1):
        host_count = 0
        result_list = []
        for cnt in range(0, len(list1)):
            result = dict()
            if list1[cnt] == "Nmap" and list1[cnt + 2] == "scan" and list1[cnt + 4] == "report" and list1[
                        cnt + 6] == "for":
                host_count += 1
                cnt1 = 8
                ip_addr = ''
                while list1[cnt + cnt1] != "\n":
                    if type(list1[cnt + cnt1]) == str:
                        ip_addr = ip_addr + list1[cnt + cnt1]
                    cnt1 = cnt1 + 1
                # self.print('\n\n HOST %s IS %s \n' % (host_count, ip_addr))
                result['ip_address'] = ip_addr

            elif list1[cnt] == "PORT" and list1[cnt + 2] == "STATE" and list1[cnt + 4] == "SERVICE":
                result['post_state_service'] = []
                cnt2 = 6
                openPort = True
                value = True
                # self.print('  PORT', 'STATE'.rjust(15), 'SERVICE'.rjust(15))
                # self.print("\t\t PORT \t\t\t\t STATE \t\t\t SERVICE \n")
                while value == True and cnt2 % 6 == 0:
                    try:
                        check = int(list1[cnt + cnt2][0])
                        value = True
                    except:
                        value = False
                        break
                    # self.print(' ', list1[cnt + cnt2], list1[cnt + cnt2 + 2].rjust(13), list1[cnt + cnt2 + 4].rjust(13))
                    # self.print("\t\t %s \t\t\t %s \t\t\t %s \n" % (
                    result['post_state.service'].append(list1[cnt + cnt2], list1[cnt + cnt2 + 2], list1[cnt + cnt2 + 4])
                    cnt2 += 6

            elif list1[cnt] == "MAC" and list1[cnt + 2] == "Address:":
                cnt1 = 4
                mac_addr = ''
                while list1[cnt + cnt1] != "\n":
                    if type(list1[cnt + cnt1]) == int:
                        list1[cnt + cnt1] = ' '
                    mac_addr += list1[cnt + cnt1]
                    cnt1 = cnt1 + 1
                # self.print(" MAC ADDRESS %s \n" % mac_addr)
                result['mac_address'] = mac_addr
            elif list1[cnt] == "OS" and list1[cnt + 2] == "details:":
                cnt1 = 4
                os = ''
                while list1[cnt + cnt1] != "\n":
                    if type(list1[cnt + cnt1]) == int:
                        list1[cnt + cnt1] = ' '
                    os += list1[cnt + cnt1]
                    cnt1 = cnt1 + 1
                # self.print(" OS DETAIL  %s  \n " % os)
                result['os'] = os
            elif list1[cnt] == "Device" and list1[cnt + 2] == "type:":
                cnt1 = 4
                dev_type = ''
                while list1[cnt + cnt1] != "\n":
                    if type(list1[cnt + cnt1]) == int:
                        list1[cnt + cnt1] = ' '
                    dev_type += list1[cnt + cnt1]
                    cnt1 = cnt1 + 1
                # self.print(" DEVICE TYPE %s \n" % dev_type)
                result['device'] = dev_type

            result_list.append(result)
        # self.print("\n\n YOU HAVE %s HOST(S) UP" % host_count)
        return result_list


        # v = Netscan()
        # w = v.parser("ifconfig")
        # x = v.getIpMask(w)
        # print(" SCANNING... ")
        # y = v.parser("nmap", "-O", x)
        # v.scanResult(y)
