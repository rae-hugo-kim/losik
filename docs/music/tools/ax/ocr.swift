import Foundation
import Vision
import AppKit
let args = CommandLine.arguments
let path = args[1]; let scale = Double(args.count > 2 ? args[2] : "2")!
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { exit(1) }
let W = Double(cg.width), H = Double(cg.height)
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.recognitionLanguages = ["ko-KR", "en-US"]
req.usesLanguageCorrection = false
let h = VNImageRequestHandler(cgImage: cg, options: [:])
try! h.perform([req])
for o in req.results ?? [] {
  guard let c = o.topCandidates(1).first else { continue }
  let b = o.boundingBox
  let x = b.origin.x * W / scale, y = (1 - b.origin.y - b.size.height) * H / scale
  let w = b.size.width * W / scale, hh = b.size.height * H / scale
  print("\(Int(x)),\(Int(y)),\(Int(w)),\(Int(hh))\t\(c.string)")
}
