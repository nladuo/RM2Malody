import json
import struct


def convert_imd_to_mc_slide(song, ch_name):
    f = open(f"节奏大师官方谱/{song}_4k_hd.imd", 'rb')
    f.seek(0, 0)

    length = struct.unpack('i', f.read(4))[0]
    print(length)

    count = struct.unpack('i', f.read(4))[0]
    print(count)

    for i in range(count):
        t = struct.unpack('i', f.read(4))
        bpm = struct.unpack('d', f.read(8))
        if i == 0:
            print(t, bpm)

    flag = struct.unpack('h', f.read(2))[0]
    count = struct.unpack('i', f.read(4))[0]
    key = 0
    print(flag, count)
    d = []
    for i in range(count):
        action = struct.unpack('h', f.read(2))[0]
        time = struct.unpack('i', f.read(4))[0]
        track = struct.unpack('b', f.read(1))[0]
        param = struct.unpack('i', f.read(4))[0]
        if (time > 0) and  (time <= length):
            if action == 0x00:
                if key < track:
                    key = track
            elif action in [0x01, 0x61, 0x21, 0xA1]:
                if key < track + param:
                    key = track + param
            elif action in [0x02, 0x62, 0x22, 0xA2]:
                if (time + param > length):
                    param = length - time
                if key < track:
                    key = track

            d.append([time, track, action, param])

    key += 1

    f.close()
    print("key", key)

    print(d)

    bpm = bpm[0]
    col_list = [32, 96, 160, 224]


    one_beat = int(60*1000 / bpm)

    notes = []
    index = 0
    note = {}
    slide_notes = []
    while index < len(d):
        [time, track, action, param] = d[index]

        which_beat = [int(time / one_beat), int((time % one_beat) / one_beat * 1000), 1000]
        note = {
            "beat": which_beat,
            "x": col_list[track],
            # "w": 62
        }
        if action == 0:
            notes.append(note)
        elif action == 1:
            notes.append(note)
            _notes = []
            span = param*64
            for i in range(1, 3):
                x = int(col_list[track] + span*i/2)
                t = time + int(i*one_beat/16)
                _notes.append({
                    "beat": [int(t / one_beat), int((t % one_beat) / one_beat * 1000), 1000],
                    "x": x,
                    "w": 62,
                    "type": 4
                })
            notes += _notes
        elif action == 2:
            note["seg"] = [{
                "beat": [int(param / one_beat), int((param % one_beat) / one_beat * 1000), 1000],
                "x": 0,
            }]
            notes.append(note)
        else:
            slide_notes.append([time, track, action, param])

        index += 1


    print(slide_notes)
    id_selected = []
    slides = []

    while len(id_selected) != len(slide_notes):
        one_slide = []
        for i, note in enumerate(slide_notes):
            if i in id_selected:
                continue
            if len(one_slide) == 0:
                one_slide.append(note)
                id_selected.append(i)
            else:
                last_note = one_slide[-1]
                if last_note[2] == note[2]:
                    continue
                if note[3] <= 3:
                    if ((last_note[0] + last_note[3]) == note[0]) and (last_note[1] == note[1]):
                        one_slide.append(note)
                        id_selected.append(i)
                    elif ((last_note[0] + last_note[3] + 1) == note[0]) and (last_note[1] == note[1]):
                        one_slide.append(note)
                        id_selected.append(i)
                    elif ((last_note[0] + last_note[3] - 1) == note[0]) and (last_note[1] == note[1]):
                        one_slide.append(note)
                        id_selected.append(i)
                else:
                    if (last_note[0] == note[0]) and ((last_note[1] + last_note[3]) == note[1]):
                        one_slide.append(note)
                        id_selected.append(i)
            if (note[2] == 162) or (note[2] == 161):
                break

        slides.append(one_slide)
    # print(slides)
    col_list_slide = [44, 99, 154, 210]
    # col_list_slide = [32, 96, 160, 224]
    for one_slide in slides:
        _len = len(one_slide)
        index = 0
        [time, track, action, param] = one_slide[index]
        which_beat = [int(time / one_beat), int((time % one_beat) / one_beat * 1000), 1000]
        note = {
            "beat": which_beat,
            "x": col_list_slide[track],
            "w": 90,
            "seg": []
        }

        index += 1
        if _len == 1:
            del note["seg"]
            notes.append(note)
            _notes = []
            span = param * 55
            for i in range(1, 3):
                x = int(col_list[track] + span*i/2)
                t = time + int(i*one_beat/16)
                _notes.append({
                    "beat": [int(t / one_beat), int((t % one_beat) / one_beat * 1000), 1000],
                    "x": x,
                    "w": 62,
                    "type": 4
                })
            notes += _notes
            continue

        next_note = one_slide[index]
        start_offset = 0
        start_t = time

        while index < _len:
            if param < 3:  # 如果是滑长条
                offset = param * 55
                start_offset += offset
                _t = next_note[0] + next_note[3] - time
                if _t > (one_beat*0.3):
                    _t = time + (one_beat*0.3) - start_t

                note["seg"].append({
                    "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                    "x": start_offset,
                    "w": 90,
                })
                if _t > (one_beat * 0.3):
                    _t = next_note[0] + next_note[3] - start_t
                    note["seg"].append({
                        "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                        "x": start_offset,
                        "w": 90,
                    })
            else:
                offset_t = param - int(0.3 * one_beat)
                if offset_t > 0:
                    _t = time - start_t + offset_t
                    note["seg"].append({
                        "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                        "x": start_offset,
                        "w": 90,
                    })

                offset_t = 0
                offset = next_note[3] * 64
                start_offset += offset
                _t = time + param - start_t
                note["seg"].append({
                    "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                    "x": start_offset,
                    "w": 90,
                })

            index += 1
            if index >= _len:
                [time, track, action, param] = next_note
                if param < 3:
                    pass
                else:
                    _t = time + param - start_t
                    note["seg"].append({
                        "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                        "x": start_offset,
                        "w": 90,
                    })
                break
            [time, track, action, param] = one_slide[index]
            index += 1

            if index >= _len:
                if param < 3:
                    pass
                else:
                    _t = time + param - start_t
                    note["seg"].append({
                        "beat": [int(_t / one_beat), int((_t % one_beat) / one_beat * 1000), 1000],
                        "x": start_offset,
                        "w": 90,
                    })
                break
            else:
                next_note = one_slide[index]

        # print(note)
        # exit()
        notes.append(note)


    # print(notes)
    # exit()
    # print(notes)
    notes.append({
        "beat": [0, 0, 1],
        "sound": f"{song}.mp3",
        "vol": 100,
        "type": 1
    })

    data = {
        "meta": {
            "$ver": 0,
            "creator": "nladuo",
            "background": f"{song}.jpg",
            "version": f"{ch_name}_4k_Hard",
            "id": 0,
            "mode": 7,
            "time": 1553609049,
            "song": {
                "title": "节奏大师4k官谱转谱",
                # "title": f"{ch_name}",
                "artist": "节奏大师",
                "id": 0
            },
            "mode_ext": {}
        },
        "time": [{
            "beat": [0, 0, 1],
            "bpm": bpm
        }],
        "effect": [],
        "note": notes,
        "extra": {
            "test": {
                "divide": 4,
                "speed": 100,
                "save": 0,
                "lock": 0,
                "edit_mode": 0
            }
        }
    }

    return data


