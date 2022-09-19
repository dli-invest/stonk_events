package main

import (
	// "os"

	"github.com/dli-invest/finreddit/pkg/reddit"
)

func main() {
	reddit.ScanSRs("investing.yml")
	// argsWithProg := os.Args
	// if len(argsWithProg) > 1 {
	// 	reddit.ScanSRs(argsWithProg[1])
	// } else {
	// 	panic("No arguments passed in")
	// }

}
