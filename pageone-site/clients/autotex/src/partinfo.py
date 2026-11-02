"""General mechanical knowledge per part type, used on the brand x part pages (e.g. /kia/front-brake-pads/).
These are general facts about how the part works and how it fails. They are NOT claims about Autotex stock, warranty or fitting.
id: dict(what = one line on the job the part does,
         signs = common signs it is worn or failing,
         fit = what decides which version fits a given car,
         send = what to send Autotex besides the chassis number / photo)"""

I = {}
def add(pid, what, signs, fit, send):
    I[pid] = dict(what=what, signs=signs, fit=fit, send=send)

add("front-bumper", "covers and protects the front of the car and carries the grille opening, fog lamp openings and sensor brackets",
    ["cracks, split mounting tabs or a bumper that sags after a knock", "paint damage or deep scrapes after a parking bump", "gaps along the bonnet or fender edge because the clips have broken"],
    "generation, facelift and trim level; fog lamps, parking sensors and the grille design change the bumper shape and cut-outs",
    "a photo of the front from the front and the side, and whether the car has fog lamps or parking sensors")
add("rear-bumper", "covers the back of the car and carries the reflectors, parking sensors and the exhaust cut-out on some trims",
    ["cracks or split mounting tabs after a reversing knock", "a bumper edge that has popped out of the tail lamp or boot gap", "paint damage that has exposed the plastic"],
    "generation and facelift; parking sensor holes and exhaust cut-outs differ by trim",
    "a photo of the rear and whether the car has parking sensors")
add("bonnet", "is the hinged panel over the engine bay, made of steel or aluminium depending on the car",
    ["dents or creases after an accident or a fallen branch", "rust or bubbling paint along the front edge", "a latch that does not close or a bonnet that sits uneven against the fenders"],
    "generation and facelift; the shape of the front edge follows the headlamp and grille design",
    "a photo of the front of the car with the bonnet closed")
add("front-grille", "is the grille in the front bumper opening that lets air to the radiator and carries the badge area",
    ["broken slats or missing clips after a knock", "chrome peeling or fading", "a loose grille that rattles at speed"],
    "generation, facelift and trim; the grille design is one of the first things to change at a facelift",
    "a photo of the front of the car, and the trim level if you know it")
add("front-fender", "is the body panel beside the bonnet that covers the front wheel arch",
    ["dents or creases from a side knock", "rust around the wheel arch lip or the lower edge", "a panel gap against the door or bonnet after repair"],
    "generation, and left or right side; the lamp and side-repeater cut-outs can differ by facelift",
    "a photo of the damaged side and whether you need the left or right fender")
add("side-mirror", "gives the view along the car sides and, on many cars, folds, heats or carries the turn signal",
    ["a cracked or loose mirror housing, or glass that vibrates", "a power fold or adjustment motor that has stopped working", "a turn signal in the mirror that no longer lights"],
    "generation and trim; the number of wires depends on power fold, heating, camera and blind spot features, and the part is sold left or right",
    "a photo of the back of the mirror showing the plug, and whether it is the driver or passenger side")
add("wiper-blades", "clear rain from the windscreen with a rubber edge pressed against the glass",
    ["streaks or smears that do not clear", "chattering or squeaking as the blade crosses the glass", "split or hardened rubber"],
    "blade length for each side and the type of arm connector; the driver and passenger blades are often different lengths",
    "a photo of the old blade at the arm end, and the car plate or chassis number")
add("headlamp", "lights the road ahead and, on many cars, houses the daytime running light and turn signal",
    ["yellowed, hazy or cracked lens that lowers the light output", "moisture inside the lamp", "a broken mounting tab, or a beam that cannot be aimed properly"],
    "generation, facelift, left or right side and the bulb type (halogen, HID or LED); the same model can have different lamps by trim",
    "a photo of the front of the lamp and the back with its plug, and which side")
add("tail-lamp", "carries the brake, tail, reverse and turn signal lights at the back of the car",
    ["a cracked lens that lets in water", "moisture or fogging inside the lamp", "a brake light or turn signal that no longer works because the circuit board or socket has burnt"],
    "generation, facelift and side; sedan and hatchback bodies, and LED against bulb versions, use different lamps",
    "a photo of the lamp from behind the car and from inside the boot, and which side")
add("fog-lamp", "is the low lamp in the bumper that lights the road edge in rain or haze",
    ["a cracked lens or a broken bracket", "water inside the lamp", "a lamp that stays dark even with a new bulb"],
    "generation, facelift and side; the lamp must match the bumper opening, so trims without fog lamps have a blank cover instead",
    "a photo of the front bumper and the lamp, and which side")
add("front-brake-pads", "are the friction pads that clamp the front discs to slow the car, and they do most of the braking",
    ["a squeal when braking, often from the metal wear indicator", "a longer stopping distance or a soft, low pedal", "a brake warning light on cars with a pad sensor"],
    "model, generation and the front caliper and disc size; different trims of one model can use different pad sizes",
    "a photo of the old pads and the disc size if you have it")
add("rear-brake-pads", "are the friction pads at the rear axle that balance the braking and hold the car on a slope",
    ["a squeal or grinding from the rear when braking", "a brake warning light on cars with a pad sensor", "uneven wear between the left and right pads"],
    "model and generation, and whether the rear brake is a disc or a drum; the rear pads are a different part from the front",
    "a photo of the old pads, and whether the car has an electric parking brake")
add("front-brake-discs", "are the steel discs the front pads clamp on, sold in pairs so both sides brake evenly",
    ["a shudder in the pedal or steering wheel when braking", "a deep lip at the disc edge or scoring on the face", "the disc is below the minimum thickness stamped on it"],
    "model, generation and disc diameter; some trims have larger or vented discs",
    "a photo of the disc and its diameter or thickness if known")
add("rear-brake-discs", "are the discs at the rear axle, sold in pairs, on cars with rear disc brakes",
    ["a pulsing feel through the pedal when braking", "scoring or a deep lip on the disc face", "rust that does not clear after a few stops"],
    "model and generation, and whether the car has rear discs at all, since some trims have drums; the disc may also have an integrated parking brake drum",
    "a photo of the rear disc and whether the car has an electric parking brake")
add("front-shock-absorber", "controls the up and down movement of the front wheel so the car stays steady over bumps",
    ["a bouncy ride that keeps moving after a bump", "oil leaking down the body of the absorber", "a knocking noise over speed bumps or the front dipping hard under braking"],
    "model and generation, and the left or right side; the part may be sold as the absorber alone or with the spring and mounts as a strut",
    "a photo of the absorber showing any leak, and which side")
add("rear-shock-absorber", "controls the movement of the rear wheels and keeps the back of the car from bouncing",
    ["the rear bouncing or wallowing after bumps", "oil leaking along the body", "a knock from the rear over bumps"],
    "model and generation, and the left or right side; the mount style differs between hatchbacks, sedans and SUVs",
    "a photo of the absorber, and whether you also want the stopper and top mount")
add("lower-control-arm", "links the wheel hub to the body at the bottom of the front suspension and holds the wheel in place",
    ["a clunk over bumps from the front", "uneven or fast tyre wear and a car that pulls to one side", "a cracked bush or a worn ball joint on the arm"],
    "model, generation and side; the arm may come with the ball joint and bushes or as a bare arm",
    "a photo of the arm and which side")
add("stabilizer-link", "joins the anti roll bar to the front strut so the car leans less in corners",
    ["a rattle or clunk over small bumps at low speed", "more body roll in corners", "a loose or torn rubber boot on the link"],
    "model and generation, and the side; links come in different lengths for different trims",
    "a photo of the link and which side")
add("tie-rod-end", "joins the steering rack to the wheel so the wheel turns when you steer",
    ["a clunk or looseness in the steering", "uneven tyre wear on the inner edge", "the car drifts or the steering wheel shakes at speed"],
    "model, generation and side, plus the thread and taper size of the end",
    "a photo of the old end and which side; an alignment is usually needed after fitting")
add("wheel-bearing", "lets the front wheel spin freely on its hub with little friction",
    ["a humming or growling noise that rises with speed and changes when you turn", "play in the wheel when it is rocked by hand", "a vibration that follows speed rather than engine revs"],
    "model, generation and side, and whether the bearing is sold alone or inside the hub unit; ABS sensor rings change the type",
    "a photo of the old hub or bearing, and which side")
add("engine-mount", "holds the engine to the body and absorbs its vibration; it is rubber, sometimes filled with fluid",
    ["more vibration in the cabin at idle", "a knock when you pull away or change gear", "the engine rocking visibly when revved"],
    "model, generation, engine and gearbox, since each car has several mounts in different positions",
    "which mount you suspect (top, side or lower torque mount) and when the noise happens")
add("gearbox-mount", "holds the gearbox to the body and takes the twist when the car pulls away",
    ["a clunk when you shift between Drive and Reverse", "vibration felt in the floor", "a cracked or collapsed rubber on the mount"],
    "model, generation and gearbox type (automatic or manual); the mount differs between them",
    "when the clunk happens and a photo of the mount if it can be seen")
add("spark-plugs", "ignite the fuel and air in each cylinder of a petrol engine, so a set covers every cylinder",
    ["a rough idle or hesitation when you accelerate", "harder starts and higher fuel use", "a misfire that sets the check-engine light"],
    "engine, since plug type, heat range and gap change by engine; the number of plugs is the number of cylinders",
    "the engine size, and the mileage since the last plug change")
add("ignition-coil", "turns the battery voltage into the spark voltage each plug needs, often one coil per cylinder",
    ["a rough or shaky idle, especially when warm", "hesitation or jerking under acceleration", "a flashing check-engine light while the engine misfires"],
    "engine and generation; coil shape and connector change with the engine, and the part is sold per coil",
    "which cylinder is misfiring if the fault code says so")
add("oil-filter", "traps dirt and metal particles in the engine oil as it circulates",
    ["oil that looks very dark and gritty soon after a change", "the oil pressure warning flashing at idle", "the filter is overdue by mileage or time"],
    "engine, since the filter may be a cartridge element or a spin-on canister and the thread differs",
    "the engine size and fuel type")
add("air-filter", "stops dust and debris entering the engine intake",
    ["dust or leaves in the airbox", "weaker acceleration or higher fuel use", "a filter that looks dark and clogged when held to light"],
    "engine and generation; the panel size changes with the airbox",
    "a photo of the old filter, and the engine size")
add("drive-belt", "turns the alternator, aircon compressor and sometimes the water pump from the engine",
    ["a squeal at start up or when the aircon engages", "cracks, fraying or missing ribs on the belt", "a flat battery or an overheating engine if the belt slips or snaps"],
    "engine and options; a car with aircon and power steering pump uses a longer belt than one without, and the rib count and length matter",
    "the engine size, whether the car has aircon, and a photo of the old belt")
add("water-pump", "circulates coolant through the engine and radiator",
    ["coolant dripping from the pump weep hole", "a whine or grinding from the front of the engine", "the engine overheating with no other cause"],
    "engine; the pump may be driven by the drive belt or the timing belt, and some come with a housing",
    "the engine size and whether the pump is on the timing or the drive belt")
add("thermostat", "opens at a set temperature to let hot coolant to the radiator, then closes to hold the engine at working temperature",
    ["an engine that overheats or runs cold", "a temperature gauge that swings", "poor heater output because the engine never warms up"],
    "engine, and the opening temperature; the part may come with its housing",
    "the engine size and what the temperature gauge does")
add("radiator", "cools the engine coolant by passing it through thin fins in the airflow",
    ["coolant leaks or green, pink or orange stains under the front of the car", "overheating in traffic", "a blocked core or damaged fins"],
    "model, generation and engine; the core size, outlets and whether the car is manual or automatic change the radiator",
    "a photo of the old radiator or the leak, and whether the gearbox is automatic")
add("radiator-fan", "pulls air through the radiator when the car is slow or stopped, and cools the aircon condenser too",
    ["the engine temperature rising in traffic", "a fan that never spins or runs loudly", "an aircon that blows warm at a standstill"],
    "model, generation and engine; the shroud, blade count and plug differ",
    "when the car overheats and a photo of the fan plug")
add("aircon-compressor", "pumps and pressurises the refrigerant so the aircon can cool",
    ["warm air from the vents with the aircon on", "a grinding or rattling noise when the aircon is switched on", "the clutch plate not engaging or oil spray around the compressor"],
    "engine and compressor type, plus the pulley and plug; two engine options in one model may use different compressors",
    "a photo of the compressor label and plug, and the engine size")
add("aircon-condenser", "sits in front of the radiator and releases heat from the refrigerant so it turns back into liquid",
    ["an aircon that is cool at speed but warm in traffic", "oily stains or damage on the fins from a stone strike or a leak", "refrigerant that keeps leaking after a regas"],
    "model and generation, and the pipe positions and core size",
    "a photo of the condenser if visible and the leak if known")
add("cabin-filter", "filters dust and pollen from the air blown into the cabin through the aircon",
    ["weaker airflow from the vents", "a musty or dusty smell when the aircon starts", "visible dirt or leaves in the filter"],
    "model and generation; the filter size and its position (behind the glovebox in many cars) differ",
    "a photo of the old filter")
add("alternator", "charges the battery and runs the electrics while the engine is running",
    ["the battery light on the dashboard", "dim lights or slow wipers at idle", "a whine or a burning smell from the front of the engine"],
    "engine, output in amps and the connector and pulley type",
    "a photo of the alternator label, and the engine size")
add("starter-motor", "turns the engine over to start it",
    ["a click but no crank, or a slow crank with a good battery", "a grinding noise after the engine has started", "intermittent starting that comes and goes"],
    "engine and gearbox, plus the mounting and plug",
    "a photo of the starter label, and whether the car is petrol or diesel")
add("engine-oil", "lubricates and cools the moving parts of the engine; the grade and the amount depend on the engine",
    ["the oil change interval has passed by distance or time", "oil that is thick, black or gritty on the dipstick", "a noisier engine or a rising oil temperature"],
    "the oil grade (for example 0W-20 or 5W-30) and the capacity for the engine",
    "the engine size and the oil you used last time if you remember it")
add("transmission-oil", "lubricates and cools the gearbox, and in an automatic also carries the pressure that shifts the gears",
    ["rough or delayed shifts", "a burnt smell or dark oil on the dipstick", "the gearbox is due for a fluid change by distance"],
    "the gearbox fluid type, which differs between a conventional automatic, a dual clutch (DCT) and a CVT; the wrong fluid can damage the gearbox",
    "the gearbox type, which a chassis number identifies")
add("strut-top-mount", "joins the top of the front strut to the body and lets the strut turn with the steering",
    ["a knocking or creaking from the front when turning or over bumps", "a worn rubber that has cracked or split", "uneven steering feel after the car has been lowered or changed"],
    "model and generation, and the side; usually changed together with the absorber",
    "a photo of the old mount and which side")
add("strut-bearing", "sits in the top mount so the spring and strut turn smoothly when steering",
    ["a creak or groan from the front when turning the steering wheel at low speed", "a notchy or heavy steering feel", "a knock from the top of the strut"],
    "model and generation; the bearing may be separate or part of the top mount",
    "a photo of the old bearing and which side")
add("control-arm-bush", "is the rubber sleeve at the pivot points of the control arm that absorbs road shock",
    ["a clunk when braking or going over bumps", "the car wandering or pulling when you brake", "visible cracks or a split in the rubber"],
    "model and generation, and which bush (front, rear or hydraulic); the side matters",
    "a photo of the arm and the bush position")
add("rear-bump-stop", "is the rubber stopper on the rear absorber that limits the travel before the suspension bottoms out",
    ["a knock from the rear on big bumps", "a cracked, crumbled or missing rubber", "the rear sitting low or bottoming out"],
    "model and generation, and the side; changed with the rear absorber",
    "a photo of the old stopper and which side")
add("rear-top-mount", "joins the top of the rear absorber to the body on cars that use a rear top mount",
    ["a clunk from the rear over bumps", "a cracked or split rubber", "the rear absorber moving in its seat"],
    "model and generation; not every model uses one, so the chassis number matters",
    "a photo of the old mount and which side")
add("steering-rack", "turns the steering wheel movement into the wheel angle, assisted by hydraulic or electric power",
    ["oil leaking from the rack boots or a wet rack", "heavy steering, a whine on turning or a clunk at the wheel", "play in the steering wheel"],
    "model and generation, and whether the assist is hydraulic or electric; left and right hand drive racks differ",
    "a photo of the rack and its label, and whether the steering is power or electric")
add("radiator-cap", "holds the cooling system at a set pressure so the coolant boils at a higher temperature",
    ["coolant spilling from the reservoir or the cap", "a cracked or loose seal", "overheating with no leak found"],
    "the pressure rating stamped on the cap and the neck shape; check it matches the radiator",
    "a photo of the old cap and the pressure printed on it")
add("valve-cover-gasket", "seals the valve cover to the top of the engine so oil stays inside",
    ["oil seeping on the top or side of the engine", "a burning oil smell from the hot exhaust", "oil on the spark plug wells"],
    "engine; the gasket is cut to the cover, and may come with the plug well seals",
    "the engine size and where the oil is seeping")
add("crankshaft-sensor", "reads the crankshaft position so the engine computer times the spark and fuel",
    ["a long crank or an engine that will not start", "stalling when warm", "a check-engine light with a crank position fault code"],
    "engine and generation, and the connector and mounting",
    "the fault code if you have one, and the engine size")
add("camshaft-sensor", "reads the camshaft position so the engine computer times the fuel and valve timing",
    ["a rough start or hesitation", "the check-engine light with a camshaft position code", "reduced power or the engine going into limp mode"],
    "engine and generation, and which camshaft (intake or exhaust) on twin-cam engines",
    "the fault code if you have one, and the engine size")
add("fuel-pump", "pushes fuel from the tank to the engine at the right pressure, usually mounted inside the tank",
    ["a whine from the rear seat area", "the engine cutting out under load or struggling to start", "a long crank when the tank is low"],
    "model, generation and fuel (petrol or diesel); the module may include the filter and level sender",
    "the fuel type and whether the engine stalls under load")
add("purge-valve", "is the solenoid that lets fuel vapour from the charcoal canister into the engine",
    ["a rough idle after refuelling", "a check-engine light with an EVAP code", "difficulty starting after filling the tank"],
    "engine and generation, and the plug and hose connections",
    "the fault code if you have one")
add("belt-tensioner", "keeps the drive belt at the right tension",
    ["a squeal or a belt that flutters", "a tensioner arm that wobbles or a noisy pulley", "uneven wear on the belt"],
    "engine and options, since the tensioner depends on the belt route and aircon",
    "the engine size and a photo of the belt route")
add("door-hinge", "carries the weight of the door and lets it swing",
    ["a door that sags and drops when you open it", "a creak or a door that does not latch squarely", "play when the open door is lifted"],
    "model, door position (front or rear) and side, and whether it is the upper or lower hinge",
    "a photo of the hinge, and which door")
add("door-handle", "is the outer handle that releases the door latch",
    ["a handle that feels loose or snaps back slowly", "a cracked or broken handle", "a door that no longer opens from the outside"],
    "model, door position and side, and whether the handle has a keyless entry sensor or a key cylinder",
    "a photo of the handle, and which door")
add("boot-lock", "latches the boot or tailgate shut and releases it from the key or switch",
    ["a boot that will not open or will not latch", "a lock that jams or spins with the key", "an alarm or boot warning light when the boot is closed"],
    "model and generation, and whether the latch is mechanical or electric",
    "a photo of the lock and whether the key turns")
add("boot-switch", "is the switch that opens the boot or tailgate from the outside or from the driver seat",
    ["the boot no longer opens from the button", "an intermittent button", "moisture or corrosion in the switch"],
    "model and generation; the plug and the position (handle or badge) differ",
    "a photo of the switch and its plug")
add("ball-joint", "is the pivot between the control arm and the wheel hub that lets the wheel move and steer",
    ["a clunk over bumps and when turning", "uneven tyre wear and a loose feeling front end", "a torn boot with grease coming out"],
    "model and generation, and side; some arms have a bolt-in joint and others are pressed in",
    "a photo of the old joint and which side")
add("power-window-switch", "controls the electric windows from the driver door or a passenger door",
    ["a window that works from one switch but not another", "buttons that stick or are intermittent", "the auto up or down function that has stopped"],
    "model, generation and the number of windows the switch controls; the master switch on the driver door is different from a single switch",
    "a photo of the switch and which door it is on")
add("thermostat-housing", "is the outlet or housing around the thermostat where hoses join the engine",
    ["coolant seeping around the housing", "a crack or a corroded seat", "an overheating engine with low coolant"],
    "engine and generation, and the number of outlets",
    "the engine size and a photo of the housing")
add("upper-radiator-hose", "carries hot coolant from the engine to the top of the radiator",
    ["a swollen, soft or hard cracked hose", "coolant drips at the clamp", "overheating from a collapsed hose"],
    "engine and options, since the length and the shape of the bends depend on the model",
    "a photo of the old hose and the engine size")
add("lower-radiator-hose", "carries cooled coolant from the bottom of the radiator back to the engine",
    ["a hose that collapses when the engine cools", "coolant dripping at the clamp or from a crack", "an overheating engine"],
    "engine and options, since the length and the shape of the bends depend on the model",
    "a photo of the old hose and the engine size")

MISSING = None
