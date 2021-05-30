<p align="center">
  <img src="https://raw.githubusercontent.com/hughcoleman/lorenz/files/c_lorenz_ag.png" />
</p>

<p align="center">
  <b>A historically accurate simulator of the Lorenz SZ40 Cipher Machine</b>
</p>

The Lorenz machines were a set of electro-mechanical cipher machines used by the German High Command during World War II. They were developed by C. Lorenz AG in Berlin. At its core, the machines were essentially (flawed) pseudorandom number generators that encrypted and/or decrypted streams using the [Vernam cipher](https://en.wikipedia.org/wiki/Gilbert_Vernam#The_Vernam_cipher).

British cryptanalysts dubbed the machine, and its traffic, "Tunny," and managed to deduce its structure three years before they saw one themselves.

This library provides methods for simulating encryption/decryption operations on a SZ40-model Lorenz machine.

###### Usage

Import the `SZ40` class from `lorenz.machines` module, and pass the positions of the 501 cams to its constructor. Some sample patterns (`KH_CAMS`, `ZMUG_CAMS`, and `BREAM_CAMS`) are provided in the `lorenz.patterns` module.

To perform an encryption or decryption operation, pass a list of five-bit integers in MSB-first ITA2 format to the `.feed()` instance method.

```python
from lorenz.machines import SZ40
from lorenz.patterns import KH_CAMS

# import telegrahy utility library
from lorenz.telegraphy import Teleprinter

# encode the message as five-bit ITA2
message = Teleprinter.encode("ATTACK99AT99DAWN")

# use the `KH` pattern to encrypt the message.
machine = SZ40(KH_CAMS)
ciphertext = machine.feed(message)

print(Teleprinter.decode(ciphertext)) # 9W3UMKEGPJZQOKXC
```

This sample program has been designed to match [this CyberChef recipe](https://gchq.github.io/CyberChef/#recipe=Lorenz('SZ40','Custom',false,'Send','ITA2','Plaintext','5/8/9',1,1,1,1,1,1,1,1,1,1,1,1,'x.x...xx.x.x..xxx.x.x.xxxx.x.x.x.x.x..x.xx.','x.xx.x.xxx..x.x.x..x.xx.x.xxx.x....x.xx.x.x.x..','x.x.x.x..xxx....x.x.xx.x.x.x..xxx.x.x..x.x.xx..x.x.','..xx...xxxxx.x.x.xx...x.xx.x.x..x.x.xx.x..x.x.x.x.x.x','.xx...xx.x..x.xx.x...x.x.x.x.x.x.x.x.xx..xxxx.x.x...xx.x..x','.x.x.x.x.x.x...x.x.x...x.x.x...x.x...','..xxxx.xxxx.xxx.xxxx.xx....xxx.xxxx.xxxx.xxxx.xxxx.xxx.xxxx..','..x...xxx.x.xxxx.x...x.x..xxx....xx.xxxx.','.x..xxx...x.xxxx..xx..x..xx.xx.','...xx..x.xxx...xx...xx..xx.xx','.xx..x..xxxx..xx.xxx....x.','.xx..xx....xxxx.x..x.x.')&input=QVRUQUNLOTlBVDk5REFXTg).

Alternatively, use [the command-line program](https://github.com/hughcoleman/lorenz/blob/main/scripts/lorenz).

```bash
$ cat message
ATTACK99AT99DAWN
$ cat cams
+.++.+..+.+.+.+.+.++++.+.+.+++..+.+.++...+.
+..+.+.+.++.+....+.+++.+.++.+..+.+.+..+++.+.++.
+.+.+..++.+.+..+.+.+++..+.+.+.++.+.+....+++..+.+.+.
.+.+.+.+.+.+..+.++.+.+..+.+.++.+...++.+.+.+++++...++.
.+..+.++...+.+.++++..++.+.+.+.+.+.+.+.+...+.++.+..+.++...++
....+.+...+.+.+...+.+.+...+.+.+.+.+.+
...++++.+++.++++.++++.++++.++++.+++....++.++++.+++.++++.++++.
..++++.++....+++..+.+...+.++++.+.+++...+.
..++.++..+..++..++++.+...+++..+
.++.++..++...++...+++.+..++..
..+....+++.++..++++..+..++
..+.+..+.++++....++..++
$ ./lorenz --cams cams --positions "1-1-1-1-1,1-1,1-1-1-1-1" message
9W3UMKEGPJZQOKXC
$ ./lorenz --cams cams --positions "1-2-3-4-5,6-7,8-9-10-11-12" message
JPOMQV44BUOZAECE
```

The second example mimics [this CyberChef recipe](https://gchq.github.io/CyberChef/#recipe=Lorenz('SZ40','Custom',false,'Send','ITA2','Plaintext','5/8/9',1,47,50,51,56,33,56,35,24,21,17,13,'x.x...xx.x.x..xxx.x.x.xxxx.x.x.x.x.x..x.xx.','x.xx.x.xxx..x.x.x..x.xx.x.xxx.x....x.xx.x.x.x..','x.x.x.x..xxx....x.x.xx.x.x.x..xxx.x.x..x.x.xx..x.x.','..xx...xxxxx.x.x.xx...x.xx.x.x..x.x.xx.x..x.x.x.x.x.x','.xx...xx.x..x.xx.x...x.x.x.x.x.x.x.x.xx..xxxx.x.x...xx.x..x','.x.x.x.x.x.x...x.x.x...x.x.x...x.x...','..xxxx.xxxx.xxx.xxxx.xx....xxx.xxxx.xxxx.xxxx.xxxx.xxx.xxxx..','..x...xxx.x.xxxx.x...x.x..xxx....xx.xxxx.','.x..xxx...x.xxxx..xx..x..xx.xx.','...xx..x.xxx...xx...xx..xx.xx','.xx..x..xxxx..xx.xxx....x.','.xx..xx....xxxx.x..x.x.')&input=QVRUQUNLOTlBVDk5REFXTg). *Note that the initial positions are different*, as the CyberChef implementation (1) indexes rotor positions from 1 rather than from 0, and (2) numbers rotor positions in reverse (compared to this implementation.) Thus, to convert from our numbering system to theirs, calculate **(ROTOR SIZE - ONE-INDEXED POSITION + 2) mod ROTOR SIZE**. If the result is zero, use **ROTOR SIZE** instead.

###### References

* Diffie, W., Field, J. V., &amp; Reeds, J. A. (Eds.). (2015). *Breaking teleprinter ciphers at Bletchley Park: An edition of General report on Tunny with emphasis on statistical methods (1945)*. <!-- Hoboken, NJ: John Wiley &amp; Sons. --> [https://doi.org/10.1002/9781119061601](https://doi.org/10.1002/9781119061601)

###### License

[MIT](https://choosealicense.com/licenses/mit/)
