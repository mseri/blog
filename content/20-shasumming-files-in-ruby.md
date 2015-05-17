Id: 20,
Title: Shasumming files in ruby
Date: 2013-12-13T22:33:31.000Z
Modified: 2013-12-13T22:42:19.000Z
Tags:
Category: Blog
Slug: shasumming-files-in-ruby
Authors: Marcello Seri

Computing [SHA-\* hashes](http://en.wikipedia.org/wiki/Sha1sum) of files in ruby is in principle very easy.

You can either use the `OpenSSL` module or the `digest` one and the sytax is almost interchangeable. I am using the `digest` module just because it seems to be slightly faster (I timed it and on my machine it takes few milliseconds less).

My first code was

```
require 'digest'

filename = '/path/to/the/file'
Digest::SHA1.hexdigest(File.read(filename))
```

Then I made the hashes for a folder containing files of different sizes. For some reasones I checked them with `shasum` and with my great surprise I've discovered that some hashes (namely the ones related to files bigger than few hundred megabytes) were wrong! Remarkably, the same happened with different SHA functions, and using `openssl`.

I don't really know why the problem happened, but [apparently the solution is fairly easy](https://www.ruby-forum.com/topic/180458). I am now using a variation of the script proposed in the previous link that seems to run pretty smoothly and got rid of the error:
```
require 'digest/sha1'

filename = '/path/to/the/file'
buf = ''
d = Digest::SHA1.new
f = File.open(filename)

while not f.eof
  # reads the file in chunks of 65536 bytes
  f.read(65536, buf)
  d.update(buf)
end

d.hexdigest
```

I am using this long code just because it requires some milliseconds less than `Digest::SHA1.file(filename).hexdigest` to run (and this last is slightly faster than the `openssl` equivalent).

I hope it could be of help if you happen to have the same problem.