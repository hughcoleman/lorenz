<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3e/C._Lorenz_logo.png">
</p>

<p align="center">
  <b>A historically accurate simulator of the Lorenz SZ40 Cipher Machine.</b>
</p>

The Lorenz machines were a set of electro-mechanical cipher machines used by the German High Command during World War II. They were developed by C. Lorenz AG in Berlin. At its core, the machines were essentially (flawed) pseudorandom generators that encrypted a plaintext using the [Vernam cipher](https://en.wikipedia.org/wiki/Gilbert_Vernam#The_Vernam_cipher).

British cryptanalysts dubbed the machine and its traffic Tunny, and managed to deduce its structure three years before they ever saw the machine.

This library provides methods for simulating encryption/decryption operations on a SZ40-model Lorenz machine.

###### Usage

Import the `SZ40` class from `lorenz.sz40` to gain access to the emulator. Supply the positions of the 501 cams during instantialization. Some sample patterns are provided in `lorenz.patterns`.

The `SZ40`'s `feed` method expects a list of five-bit integers representing the input stream in MSB-first ITA2 format. A conversion utility, `lorenz.telegraphy`, is provided.

```python
from lorenz.machines import SZ40
from lorenz.patterns import KH_CAMS 
from lorenz.telegraphy import Teleprinter

# Encode the message as five-bit ITA2
message = Teleprinter.encode("ATTACK99AT99DAWN")

# Use the 'KH' pattern to encrypt the message.
machine = SZ40(KH_CAMS)
ciphertext = machine.feed(message)

print(Teleprinter.decode(ciphertext)) # 9W3UMKEGPJZQOKXC
```

This sample program has been designed to match the output of [this CyberChef recipe](https://gchq.github.io/CyberChef/#recipe=Lorenz('SZ40','Custom',false,'Send','ITA2','Plaintext','5/8/9',1,1,1,1,1,1,1,1,1,1,1,1,'x.x...xx.x.x..xxx.x.x.xxxx.x.x.x.x.x..x.xx.','x.xx.x.xxx..x.x.x..x.xx.x.xxx.x....x.xx.x.x.x..','x.x.x.x..xxx....x.x.xx.x.x.x..xxx.x.x..x.x.xx..x.x.','..xx...xxxxx.x.x.xx...x.xx.x.x..x.x.xx.x..x.x.x.x.x.x','.xx...xx.x..x.xx.x...x.x.x.x.x.x.x.x.xx..xxxx.x.x...xx.x..x','.x.x.x.x.x.x...x.x.x...x.x.x...x.x...','..xxxx.xxxx.xxx.xxxx.xx....xxx.xxxx.xxxx.xxxx.xxxx.xxx.xxxx..','..x...xxx.x.xxxx.x...x.x..xxx....xx.xxxx.','.x..xxx...x.xxxx..xx..x..xx.xx.','...xx..x.xxx...xx...xx..xx.xx','.xx..x..xxxx..xx.xxx....x.','.xx..xx....xxxx.x..x.x.')&input=QVRUQUNLOTlBVDk5REFXTg).

###### References

* [*Breaking Teleprinter Ciphers at Bletchley Park: General Report on Tunny with Emphasis on Statistical Methods* (1945)](https://doi.org/10.1002/9781119061601)

###### License

[MIT](https://choosealicense.com/licenses/mit/)
