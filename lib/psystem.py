import numpy as np
import ctypes

# Maak een voorbeeldarray
array = np.array([[1, 2], [3, 4]], dtype=np.int32)

# Toegang krijgen tot het rauwe geheugen via de buffer
buffer_pointer = array.data  # Dit is de geheugenbuffer

# Verwerk het geheugeninhoud in ctypes
size_in_bytes = array.nbytes
memory_contents = (ctypes.c_ubyte * size_in_bytes).from_address(ctypes.addressof(buffer_pointer.contents))

# Dump de bytes in hexadecimale vorm
dumped_memory = [hex(byte) for byte in memory_contents]
print("Memory contents (in hex):", dumped_memory)
