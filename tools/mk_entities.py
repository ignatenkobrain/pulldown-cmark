# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# get https://html.spec.whatwg.org/multipage/entities.json
# Usage: python tools/mk_entities.py entities.json > src/entities.rs

import json
import sys

def main(args):
	jsondata = json.loads(file(args[1]).read())
	entities = [entity[1:-1] for entity in jsondata.keys() if entity.endswith(';')]
	entities.sort()
	print """// Copyright 2015 Google Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//! Expansions of HTML5 entities

// Autogenerated by mk_entities.py

const ENTITIES: [&'static str; %i] = [""" % len(entities)
	for e in entities:
		print "        \"" + e + "\","
	print """    ];

const ENTITY_VALUES: [&'static str; %i] = [""" % len(entities)
	for e in entities:
		codepoints = jsondata['&' + e + ';']["codepoints"];
		s = ''.join(['\u{%04X}' % cp for cp in codepoints])
		print "        \"" + s + "\","
	print """    ];

pub fn get_entity(name: &str) -> Option<&'static str> {
	ENTITIES.binary_search(&name).ok().map(|i| ENTITY_VALUES[i])
}
"""

main(sys.argv)