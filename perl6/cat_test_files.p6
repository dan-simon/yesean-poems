my method lpad-lines (Str $self: Int $num) {$self.subst(/^^/, ' ' x $num, :g)}

say dir(test => /^ test .+ $/).sort.map({
    $_ ~ ":\n<pre>\n" ~ (slurp $_).chop.&lpad-lines(4) ~ "\n</pre>"
}).join("\n").&lpad-lines(4)