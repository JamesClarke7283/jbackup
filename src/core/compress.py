import zstandard
import os

class Compressor:
    @staticmethod
    def compress_file(input_file, output_file, compression_level=3, progress_callback=None):
        """
        Compress a file using zstandard compression.

        :param input_file: Path to the input file
        :param output_file: Path to the output compressed file
        :param compression_level: Compression level (1-22, default 3)
        :param progress_callback: Optional callback function to report progress
        """
        compressor = zstandard.ZstdCompressor(level=compression_level)
        
        total_size = os.path.getsize(input_file)
        compressed_size = 0

        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            with compressor.stream_writer(f_out) as compressor_stream:
                while True:
                    chunk = f_in.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    compressor_stream.write(chunk)
                    compressed_size += len(chunk)
                    if progress_callback:
                        progress = compressed_size / total_size
                        progress_callback(progress, f"Compressing: {input_file}")

    @staticmethod
    def decompress_file(input_file, output_file, progress_callback=None):
        """
        Decompress a zstandard compressed file.

        :param input_file: Path to the input compressed file
        :param output_file: Path to the output decompressed file
        :param progress_callback: Optional callback function to report progress
        """
        decompressor = zstandard.ZstdDecompressor()
        
        total_size = os.path.getsize(input_file)
        decompressed_size = 0

        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            with decompressor.stream_reader(f_in) as decompressor_stream:
                while True:
                    chunk = decompressor_stream.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    f_out.write(chunk)
                    decompressed_size += len(chunk)
                    if progress_callback:
                        progress = decompressed_size / total_size
                        progress_callback(progress, f"Decompressing: {input_file}")

    @staticmethod
    def compress_stream(input_stream, output_stream, compression_level=3):
        """
        Compress a stream using zstandard compression.

        :param input_stream: Input stream to compress
        :param output_stream: Output stream for compressed data
        :param compression_level: Compression level (1-22, default 3)
        """
        compressor = zstandard.ZstdCompressor(level=compression_level)
        compressor.copy_stream(input_stream, output_stream)

    @staticmethod
    def decompress_stream(input_stream, output_stream):
        """
        Decompress a zstandard compressed stream.

        :param input_stream: Input stream of compressed data
        :param output_stream: Output stream for decompressed data
        """
        decompressor = zstandard.ZstdDecompressor()
        decompressor.copy_stream(input_stream, output_stream)