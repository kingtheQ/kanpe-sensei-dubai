# -*- coding: utf-8 -*-
# 世界一周編 ナイロビ+賢者+券選び。会話は創作(5往復)。値段は架空。個人名なし。実在名: Java House / Artcaffe / Safaricom / Pride Lounge / Jomo Kenyatta Intl / Villa Rosa Kempinski / Turkish Airlines / Qatar Airways
D=[]
def d(id,who,bg,sp,intro,pairs,words,**kw):
    D.append(dict(id=id,who=who,bg=bg,sp=sp,intro=intro,pairs=pairs,words=words,**kw))

# ---- 達人賢者 ----
d('sage_1','達人賢者','sage','sage','星の見える広間。達人賢者が、旅のはじまりを教えてくれる。',[
("Welcome, travelers. You want to go around the world?","ようこそ、旅人たち。世界一周をしたいのですか。","*Yes*! *We* *want* to *see* *many* *airports*.","はい。たくさんの空港を見たいです。"),
("Good. One ticket can take you to many countries.","よい。1枚の航空券で、たくさんの国へ行けます。","*Really*? *How* *does* it *work*?","本当ですか。どうやって使うのですか。"),
("You choose a group of airlines. Then you fly from city to city, always going the same way around the earth.","航空会社のグループを選びます。そして、地球をいつも同じ向きに回りながら、都市から都市へ飛びます。","*I* *see*. *Where* *do* we *start*?","なるほど。どこから始めますか。"),
("Your first stop is Nairobi, in Kenya. It is a good place to practice.","最初の寄港地はケニアのナイロビです。練習にぴったりの場所です。","*Nairobi*! *Is* it *far*?","ナイロビ！遠いですか。"),
("It is a long flight. But do not worry. Speak slowly, and smile.","長い飛行です。でも心配はいりません。ゆっくり話して、笑顔でいなさい。","*Thank* you. *We* *will* *try*!","ありがとうございます。がんばります。")],
[("round the world","世界一周"),("ticket","航空券"),("airline","航空会社"),("practice","練習する"),("slowly","ゆっくり")])
d('sage_2','達人賢者','sage','sage','達人賢者に、航空券のえらび方をきいてみよう。',[
("Do you know the two big groups of airlines?","航空会社の大きなグループを2つ知っていますか。","*No*, *I* *don't*. *Please* *tell* me.","いいえ。教えてください。"),
("They are Star Alliance and oneworld. Each group has many airlines.","スターアライアンスとワンワールドです。どちらもたくさんの航空会社があります。","*What's* the *difference*?","何がちがうのですか。"),
("The airlines are different, so the routes are different. But both can take you to every airport on your list.","航空会社がちがうので、ルートもちがいます。でも、どちらでも、あなたの行きたい空港すべてに行けます。","*Can* I *change* my *mind* *later*?","あとで気が変わってもいいですか。"),
("Choose one for this trip. You can choose the other one next time.","この旅ではひとつ選びます。もうひとつは、次の機会に選べます。","*Which* *one* *is* *better*?","どちらがいいですか。"),
("Neither is better. Pick the one that feels fun. A trip should be fun!","どちらがよいということはありません。楽しそうな方を選びなさい。旅は楽しくなくては。","*Okay*. *I'll* *choose* *now*!","わかりました。いま選びます。")],
[("alliance","航空会社の連合"),("route","ルート"),("difference","ちがい"),("change my mind","気が変わる"),("choose","選ぶ")])
d('sage_3','達人賢者','sage','sage','達人賢者から、旅の英語のコツをきこう。',[
("Here is a secret about travel English. Short is good.","旅の英語のひみつを教えましょう。短くて大丈夫です。","*Short* *is* *good*? *Really*?","短くていいのですか。本当に？"),
("Yes. Say 'Excuse me,' then say what you need. People will help you.","はい。『すみません』と言ってから、必要なことを言う。人は助けてくれます。","*What* *if* I *don't* *understand*?","わからなかったらどうしますか。"),
("Say, 'Could you say that again, please?' It is very polite.","『もう一度言っていただけますか』と言いなさい。とても丁寧です。","*Could* *you* *say* *that* *again*, *please*?","もう一度言っていただけますか。"),
("Perfect! And if it is too fast, say, 'Slowly, please.'","完璧です。それでも速すぎたら、『ゆっくりお願いします』と。","*Slowly*, *please*. *I* *can* *do* *that*.","ゆっくりお願いします。できそうです。"),
("You are ready. Now, go and choose your ticket.","準備はできました。さあ、航空券を選びに行きなさい。","*Thank* *you*, *wise* *teacher*!","ありがとうございます、賢者さま。")],
[("excuse me","すみません"),("polite","丁寧な"),("again","もう一度"),("understand","理解する"),("ready","準備ができた")])

# ---- 券選び(2種類) ----
d('ticket_star','スターアライアンスの窓口係','tdesk','desk_star','スターアライアンスの窓口。ターキッシュ エアラインズで、最初の都市ナイロビへ。',[
("Welcome to the Star Alliance desk. Where are you going?","スターアライアンスの窓口へようこそ。どちらへ行かれますか。","*We* *are* *going* *around* the *world*. *First*, *Nairobi*.","世界一周です。まず、ナイロビへ。"),
("Nairobi. Very nice. May I see your passport, please?","ナイロビですね。すてきです。パスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Would you like a window seat or an aisle seat?","ありがとうございます。窓側と通路側、どちらがよいですか。","*A* *window* *seat*, *please*. *I* *want* *to* *see* *the* *clouds*.","窓側をお願いします。雲を見たいので。"),
("A window seat. Do you have any bags to check in?","窓側ですね。預ける荷物はありますか。","*Yes*, *one* *suitcase*.","はい、スーツケースがひとつです。"),
("Here is your boarding pass. Have a wonderful trip!","搭乗券です。すばらしい旅を。","*Thank* *you*! *See* *you* *in* *Nairobi*!","ありがとうございます。ナイロビでお会いしましょう。")],
[("passport","パスポート"),("window seat","窓側の席"),("aisle seat","通路側の席"),("check in","預ける・手続きする"),("boarding pass","搭乗券")])
d('ticket_ow','ワンワールドの窓口係','tdesk','desk_ow','ワンワールドの窓口。カタール航空で、最初の都市ナイロビへ。',[
("Welcome to the oneworld desk. Where are you going?","ワンワールドの窓口へようこそ。どちらへ行かれますか。","*We* *are* *going* *around* the *world*. *First*, *Nairobi*.","世界一周です。まず、ナイロビへ。"),
("Nairobi. Very nice. May I see your passport, please?","ナイロビですね。すてきです。パスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Would you like a window seat or an aisle seat?","ありがとうございます。窓側と通路側、どちらがよいですか。","*An* *aisle* *seat*, *please*. *I* *like* *to* *walk* *around*.","通路側をお願いします。歩き回るのが好きなので。"),
("An aisle seat. Do you have any bags to check in?","通路側ですね。預ける荷物はありますか。","*Yes*, *one* *suitcase*.","はい、スーツケースがひとつです。"),
("Here is your boarding pass. Have a wonderful trip!","搭乗券です。すばらしい旅を。","*Thank* *you*! *See* *you* *in* *Nairobi*!","ありがとうございます。ナイロビでお会いしましょう。")],
[("passport","パスポート"),("aisle seat","通路側の席"),("window seat","窓側の席"),("suitcase","スーツケース"),("boarding pass","搭乗券")])

# ---- 到着: ナイロビ ----
d('nbo_immig1','入国審査の係官','immig','officer','ナイロビのジョモ・ケニヤッタ国際空港に到着。入国審査の列にならんだ。',[
("Good morning. Passport, please.","おはようございます。パスポートをお願いします。","*Good* *morning*. *Here* *you* *are*.","おはようございます。どうぞ。"),
("Do you have your eTA for Kenya?","ケニアのeTA（電子渡航認証）はありますか。","*Yes*. *I* *have* *it* *on* *my* *phone*.","はい。スマホに入っています。"),
("Good. Please look at the camera.","結構です。カメラを見てください。","*Like* *this*?","こうですか。"),
("Yes, that is fine. Now, put your finger here.","はい、それでけっこうです。では、ここに指を置いてください。","*Okay*. *Is* *this* *right*?","はい。これでいいですか。"),
("All done. Welcome to Kenya!","終わりです。ケニアへようこそ。","*Thank* *you*! *Asante*!","ありがとう！アサンテ！")],
[("eTA","電子渡航認証"),("passport","パスポート"),("camera","カメラ"),("finger","指"),("welcome","ようこそ")])
d('nbo_immig2','入国審査の係官','immig','officer2','別の窓口。係官は笑顔で、ゆっくり話してくれる。',[
("Hello. What is the purpose of your visit?","こんにちは。訪問の目的は何ですか。","*I'm* *a* *tourist*. *I'm* *on* *a* *trip* *around* *the* *world*.","観光です。世界一周の旅の途中です。"),
("Wonderful! How long will you stay in Kenya?","すばらしい。ケニアにはどのくらい滞在しますか。","*For* *three* *days*.","3日間です。"),
("Where will you stay in Nairobi?","ナイロビではどこに泊まりますか。","*At* *the* *Villa* *Rosa* *Kempinski*.","ヴィラ・ローザ・ケンピンスキーです。"),
("Do you have a ticket to leave Kenya?","ケニアを出る航空券はありますか。","*Yes*. *I* *fly* *out* *in* *three* *days*.","はい。3日後に出発します。"),
("Good. Enjoy your stay. Karibu Kenya!","結構です。滞在を楽しんで。ようこそケニアへ！","*Thank* *you*. *I* *will*!","ありがとうございます。楽しみます。")],
[("purpose","目的"),("tourist","観光客"),("stay","滞在する"),("hotel","ホテル"),("leave","出発する")])
d('nbo_bag1','手荷物受け取りのスタッフ','baggage','bag_staff','手荷物受け取り。ベルトコンベアから、スーツケースが出てこない。',[
("Hello. Can I help you?","こんにちは。お手伝いしましょうか。","*Yes*. *My* *suitcase* *is* *not* *here*.","はい。スーツケースが見つかりません。"),
("I am sorry. What color is your suitcase?","申し訳ありません。スーツケースは何色ですか。","*It's* *blue*, *with* *a* *yellow* *tag*.","青で、黄色いタグがついています。"),
("May I see your baggage tag, please?","荷物のタグを見せていただけますか。","*Here* *it* *is*.","これです。"),
("Thank you. Please wait here. I will check the system.","ありがとうございます。ここでお待ちください。システムを確認します。","*How* *long* *will* *it* *take*?","どのくらいかかりますか。"),
("It is here! It came on the next belt. Enjoy Nairobi!","ありました！次のベルトで来ていました。ナイロビを楽しんで。","*Oh*, *thank* *goodness*! *Thank* *you*!","よかった！ありがとうございます。")],
[("suitcase","スーツケース"),("tag","タグ"),("belt","ベルトコンベア"),("check","確認する"),("sorry","申し訳ない")])
d('nbo_bag2','手荷物受け取りのスタッフ','baggage','bag_staff2','スーツケースを受け取ったところで、係の人に声をかけられた。',[
("Welcome to Kenya. Do you have any plastic bags in your suitcase?","ケニアへようこそ。スーツケースにレジ袋は入っていますか。","*Plastic* *bags*? *Why*?","レジ袋ですか。なぜですか。"),
("In Kenya, single-use plastic bags are not allowed. We use paper or cloth bags.","ケニアでは、使い捨てのレジ袋は禁止されています。紙か布の袋を使います。","*I* *see*. *I* *have* *a* *cloth* *bag*.","なるほど。布の袋ならあります。"),
("That is perfect. Please keep using it during your trip.","それは完璧です。旅の間、それを使ってください。","*Of* *course*. *Is* *the* *airport* *clean*?","もちろんです。空港はきれいですか。"),
("Yes, we try to keep Kenya clean and green.","はい、ケニアをきれいで緑豊かに保つようにしています。","*That's* *wonderful*.","すばらしいですね。"),
("Thank you for helping. Enjoy your trip!","協力ありがとうございます。旅を楽しんで。","*Thank* *you*. *Have* *a* *nice* *day*!","ありがとうございます。よい一日を。")],
[("plastic bag","レジ袋"),("allowed","許可されている"),("cloth","布"),("clean","きれいな"),("keep","保つ")])
d('nbo_sim1','Safaricomの店員','sim','sim_staff','到着ロビーの Safaricom の店。現地のSIMカードを買おう。',[
("Jambo! Welcome to Safaricom. How can I help?","ジャンボ！Safaricomへようこそ。ご用件は何ですか。","*I* *need* *a* *SIM* *card*, *please*.","SIMカードがほしいです。"),
("Sure. May I see your passport? We must register your SIM.","かしこまりました。パスポートを見せてください。SIMの登録が必要です。","*Here* *is* *my* *passport*.","パスポートです。"),
("Thank you. Do you want data for seven days?","ありがとうございます。7日間のデータはいかがですか。","*Yes*. *How* *much* *data* *is* *it*?","はい。データ量はどのくらいですか。"),
("Five gigabytes. It costs one thousand shillings.","5ギガバイトです。料金は1000シリングです。","*That's* *fine*. *Can* *I* *pay* *by* *card*?","けっこうです。カードで払えますか。"),
("Yes, you can. Your SIM is ready. Enjoy Kenya!","はい、できます。SIMの準備ができました。ケニアを楽しんで。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("SIM card","SIMカード"),("register","登録する"),("data","データ通信"),("gigabyte","ギガバイト"),("pay by card","カードで払う")])
d('nbo_sim2','Safaricomの店員','sim','sim_staff2','別の店員さん。スマホの設定がうまくいかないようだ。',[
("Hello. Is your phone working?","こんにちは。スマホは動いていますか。","*No*. *I* *can't* *use* *the* *internet*.","いいえ。インターネットが使えません。"),
("Let me see. Please turn your phone off and on again.","見てみましょう。スマホの電源を切って、また入れてください。","*Okay*. *Wait* *a* *moment*.","わかりました。少し待ってください。"),
("Do you see the signal bars now?","電波のバーが見えますか。","*Yes*! *I* *see* *four* *bars*.","はい！4本立っています。"),
("Good. Now open your browser and try a website.","よかった。ブラウザを開いて、サイトを見てみてください。","*It* *works*! *Thank* *you* *so* *much*.","つながりました！ありがとうございます。"),
("You are welcome. You can also use M-Pesa for payments here.","どういたしまして。ここではM-Pesaでの支払いも使えますよ。","*Great*. *I'll* *remember* *that*.","いいですね。覚えておきます。")],
[("internet","インターネット"),("turn off","電源を切る"),("signal","電波"),("browser","ブラウザ"),("payment","支払い")])
d('nbo_taxi1','タクシー乗り場の係員','taxi','taxi_staff','空港の外。ホテルまでどうやって行こう。',[
("Hello, my friend. Do you need a taxi?","こんにちは。タクシーが必要ですか。","*Yes*. *Please*. *To* *the* *Villa* *Rosa* *Kempinski*.","はい、お願いします。ヴィラ・ローザ・ケンピンスキーまで。"),
("Sure. Please wait in this line. The next car is yours.","かしこまりました。この列でお待ちください。次の車があなたたちのです。","*How* *much* *is* *it*, *please*?","料金はいくらですか。"),
("It is a fixed price. Three thousand shillings to the city.","定額です。市内まで3000シリングです。","*Okay*. *How* *long* *does* *it* *take*?","わかりました。どのくらいかかりますか。"),
("About forty minutes. The traffic is busy in the morning.","約40分です。朝は道がこみます。","*That's* *fine*. *We're* *not* *in* *a* *hurry*.","けっこうです。急いでいません。"),
("Good. Here is your car. Please watch your step.","よかった。こちらがお車です。足元にご注意ください。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("taxi","タクシー"),("fixed price","定額"),("traffic","交通量"),("busy","混んでいる"),("in a hurry","急いでいる")])
d('nbo_taxi2','ライドシェアの運転手','taxi','driver','Uber アプリで車を呼んだ。待ち合わせ場所に、車がやって来た。',[
("Hello! Are you the passengers for the hotel?","こんにちは！ホテルへ行くお客さんですか。","*Yes*, *that's* *us*. *Is* *this* *the* *Uber*?","はい、私たちです。Uberですか。"),
("Yes. May I have the last four numbers of your phone?","はい。電話番号の下4けたを教えてください。","*Sure*. *It's* *one*, *two*, *three*, *four*.","もちろん。1、2、3、4です。"),
("Perfect. Let me help with your suitcase.","ばっちりです。スーツケースをお持ちします。","*Thank* *you*. *It's* *a* *little* *heavy*.","ありがとう。少し重いんです。"),
("No problem. Do you want the air conditioner on?","問題ありません。エアコンはつけますか。","*Yes*, *please*. *A* *little* *cool*.","はい、お願いします。少し涼しく。"),
("Good. Sit back and enjoy the ride!","よし。ゆったり座って、ドライブを楽しんで。","*Thank* *you*. *Let's* *go*!","ありがとう。行きましょう！")],
[("passenger","乗客"),("suitcase","スーツケース"),("heavy","重い"),("air conditioner","エアコン"),("ride","乗ること")])

# ---- 空港: ナイロビ ----
d('nbo_java1','Java Houseの店員','cafeK','cafe_staff','Java House に入った。コーヒーのいい香り。',[
("Jambo! Welcome to Java House. What can I get you?","ジャンボ！Java Houseへようこそ。ご注文は？","*I'd* *like* *a* *latte*, *please*.","ラテをお願いします。"),
("Sure. Hot or iced?","かしこまりました。ホットですか、アイスですか。","*Hot*, *please*. *And* *a* *slice* *of* *cake*.","ホットでお願いします。それとケーキをひと切れ。"),
("We have chocolate and carrot cake. Which one?","チョコレートとキャロットのケーキがあります。どちらにしますか。","*Carrot* *cake*, *please*.","キャロットケーキをお願いします。"),
("Okay. That is eight hundred shillings.","はい。800シリングです。","*Can* *I* *pay* *by* *card*?","カードで払えますか。"),
("Yes. Here you go. Enjoy!","はい。どうぞ。ごゆっくり。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("latte","ラテ"),("iced","冷たい・氷入りの"),("slice","ひと切れ"),("carrot cake","キャロットケーキ"),("shillings","シリング(ケニアのお金)")])
d('nbo_java2','Java Houseの店員','cafeK','cafe_staff2','店は混んでいる。隣のお客さんが話しかけてきた。',[
("Excuse me. Is this seat free?","すみません。この席は空いていますか。","*Yes*, *it* *is*. *Please* *sit* *down*.","はい、空いています。どうぞ座ってください。"),
("Thank you. Are you traveling?","ありがとう。旅行中ですか。","*Yes*. *We* *are* *traveling* *around* *the* *world*.","はい。世界一周をしています。"),
("Wow! How do you like Nairobi so far?","わあ！ナイロビはここまでどうですか。","*It's* *great*. *The* *people* *are* *very* *kind*.","すばらしいです。人々がとても親切で。"),
("Thank you. You must try nyama choma before you leave.","ありがとう。帰る前にニャマチョマ（焼き肉）を食べてみて。","*Nyama* *choma*? *What* *is* *that*?","ニャマチョマ？それは何ですか。"),
("Grilled meat! It is our favorite. Enjoy your trip!","焼いたお肉です！みんな大好きなんですよ。旅を楽しんで！","*I* *will*. *Thank* *you* *for* *the* *tip*!","そうします。教えてくれてありがとう！")],
[("seat","席"),("traveling","旅行している"),("kind","親切な"),("grilled","焼いた"),("tip","アドバイス・コツ")])
d('nbo_art1','Artcaffeの店員','cafeK','cafe_staff3','Artcaffe に入った。パンのやけるにおいがする。',[
("Hello! Welcome to Artcaffe. Eat in or take away?","こんにちは！Artcaffeへようこそ。店内ですか、お持ち帰りですか。","*Eat* *in*, *please*.","店内でお願いします。"),
("Okay. Here is the menu. Would you like some water?","はい。こちらがメニューです。お水はいかがですか。","*Yes*, *please*. *What* *do* *you* *recommend*?","はい、お願いします。おすすめは何ですか。"),
("Our fresh bread and passion juice are popular.","焼きたてパンとパッションジュースが人気です。","*I'll* *have* *the* *passion* *juice*, *and* *bread*.","パッションジュースとパンをください。"),
("Good choice. Anything else?","いい選択です。ほかには？","*That's* *all*, *thank* *you*.","以上です、ありがとう。"),
("Coming right up! Please sit anywhere.","すぐお持ちします！お好きな席へどうぞ。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("eat in","店内で食べる"),("take away","持ち帰り"),("recommend","おすすめする"),("passion juice","パッションフルーツのジュース"),("popular","人気のある")])
d('nbo_art2','Artcaffeの店員','cafeK','cafe_staff4','お会計のとき、店員さんが話しかけてくれた。',[
("How was everything today?","今日はいかがでしたか。","*It* *was* *delicious*. *The* *bread* *was* *so* *soft*.","とてもおいしかったです。パンがやわらかくて。"),
("I am glad. Where are you from?","うれしいです。どちらから来ましたか。","*We* *are* *from* *Japan*.","日本からです。"),
("Japan! That is far. How long have you been traveling?","日本！遠いですね。旅はどのくらいですか。","*Only* *two* *days*. *This* *is* *our* *first* *stop*.","まだ2日です。ここが最初の寄港地です。"),
("Then you must see the animals. Nairobi National Park is close.","それなら動物を見なくちゃ。ナイロビ国立公園は近いですよ。","*Really*? *We* *would* *love* *to* *go*.","本当ですか。ぜひ行きたいです。"),
("Enjoy your trip! Come again soon.","旅を楽しんで！またいらしてくださいね。","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("delicious","おいしい"),("soft","やわらかい"),("far","遠い"),("national park","国立公園"),("close","近い")])
d('nbo_lounge1','Pride Loungeの受付','lounge','lounge_staff','Pride Lounge に着いた。受付の人がにこやかに迎えてくれる。',[
("Welcome to the Pride Lounge. May I see your boarding pass?","Pride Loungeへようこそ。搭乗券を見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Please enjoy the lounge. Do you need Wi-Fi?","ありがとうございます。どうぞお楽しみください。Wi-Fiは必要ですか。","*Yes*, *please*. *What's* *the* *password*?","はい、お願いします。パスワードは何ですか。"),
("It is on the card. Please connect to the lounge network.","カードに書いてあります。ラウンジのネットワークに接続してください。","*Thank* *you*. *Where* *can* *I* *get* *a* *drink*?","ありがとう。飲み物はどこでもらえますか。"),
("The bar is on the left. There is also food in the middle.","バーは左側です。中央には食事もあります。","*Great*. *Is* *there* *a* *quiet* *area*?","いいですね。静かな場所はありますか。"),
("Yes, at the back. Please relax and enjoy.","はい、奥にあります。ゆっくりくつろいでください。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("lounge","ラウンジ"),("password","パスワード"),("connect","接続する"),("quiet","静かな"),("relax","くつろぐ")])
d('nbo_lounge2','ラウンジの隣の席のお客さん','lounge','lounge_guest','ラウンジのソファ。隣のお客さんが笑顔であいさつしてくれた。',[
("Hello! Is this your first time in Kenya?","こんにちは！ケニアは初めてですか。","*Yes*, *it* *is*. *We* *just* *arrived*.","はい。着いたばかりです。"),
("Welcome! What are you going to do here?","ようこそ！ここで何をする予定ですか。","*We* *want* *to* *see* *the* *giraffes*.","キリンを見たいです。"),
("There is a giraffe center near Nairobi. You can feed them!","ナイロビの近くにキリンセンターがあります。えさをあげられますよ！","*That* *sounds* *fun*! *Is* *it* *safe*?","楽しそう！安全ですか。"),
("Yes. The giraffes are gentle. They love the snacks.","はい。キリンはおだやかです。おやつが大好きなんですよ。","*I* *can't* *wait*. *Thank* *you*!","待ちきれません。ありがとう！"),
("Enjoy! Safari njema! That means good journey.","楽しんで！サファリ・ンジェマ！「よい旅を」という意味です。","*Safari* *njema*! *Thank* *you*!","サファリ・ンジェマ！ありがとう！")],
[("giraffe","キリン"),("feed","えさをあげる"),("safe","安全な"),("gentle","おだやかな"),("journey","旅")])
d('nbo_duty1','免税店の店員','duty','duty_staff','免税店で、ケニアのコーヒーを見つけた。',[
("Welcome! Are you looking for something special?","いらっしゃいませ！何かお探しですか。","*Yes*. *I* *want* *Kenyan* *coffee* *for* *my* *family*.","はい。家族にケニアのコーヒーをおみやげにしたいです。"),
("Good choice. This one is from the mountains. It is very smooth.","いい選択です。これは山で育ったコーヒーです。とてもまろやかですよ。","*How* *much* *is* *it*?","いくらですか。"),
("It is twelve dollars for one bag.","1袋12ドルです。","*I'll* *take* *two* *bags*, *please*.","2袋ください。"),
("Two bags. Would you like a gift box?","2袋ですね。ギフトボックスはどうしますか。","*Yes*, *please*. *It's* *a* *present*.","はい、お願いします。プレゼントなので。"),
("Done! Here is your receipt. Thank you!","できました！レシートです。ありがとうございます！","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("coffee","コーヒー"),("smooth","まろやか"),("gift box","ギフトボックス"),("present","贈り物"),("receipt","レシート")])
d('nbo_duty2','免税店の店員','duty','duty_staff2','隣の棚には、ケニアの紅茶と、カラフルな布がならんでいる。',[
("Hello! Would you like to try some Kenyan tea?","こんにちは！ケニアの紅茶を試してみませんか。","*Yes*, *please*. *It* *smells* *nice*.","はい、お願いします。いい香りです。"),
("Here you go. Be careful. It is hot.","どうぞ。気をつけて。熱いですよ。","*Mmm*, *it's* *delicious*. *Is* *it* *strong*?","おいしい。濃いですか。"),
("A little strong. Many people add milk and sugar.","少し濃いです。ミルクと砂糖を入れる人が多いですよ。","*I'll* *buy* *a* *box* *of* *tea*.","紅茶を1箱買います。"),
("Great. And this colorful cloth is called kikoi. Do you like it?","いいですね。このカラフルな布は「キコイ」といいます。いかがですか。","*It's* *beautiful*. *I'll* *take* *a* *blue* *one*.","きれいですね。青いのをください。"),
("Lovely. Thank you for shopping with us!","すてきです。お買い上げありがとうございます！","*Thank* *you*. *Have* *a* *good* *day*!","ありがとう。よい一日を！")],
[("tea","紅茶"),("strong","濃い"),("sugar","砂糖"),("colorful","カラフルな"),("beautiful","美しい")])
d('nbo_gate1','搭乗ゲートの係員','gate','gate_agent','搭乗ゲートに着いた。アナウンスが流れている。',[
("Good afternoon. May I see your boarding pass and passport?","こんにちは。搭乗券とパスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Boarding will begin in twenty minutes.","ありがとうございます。搭乗は20分後に始まります。","*Is* *this* *the* *right* *gate*?","ここで合っていますか。"),
("Yes, this is the correct gate. Please wait over there.","はい、このゲートで合っています。あちらでお待ちください。","*Can* *I* *buy* *a* *drink* *first*?","先に飲み物を買ってもいいですか。"),
("Of course. Just come back before boarding.","もちろん。搭乗前に戻ってくればだいじょうぶです。","*Thank* *you*. *I'll* *be* *back* *soon*.","ありがとう。すぐ戻ります。"),
("No problem. Have a safe flight!","問題ありません。よい旅を！","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("gate","搭乗ゲート"),("boarding","搭乗"),("correct","正しい"),("wait","待つ"),("flight","フライト")])
d('nbo_gate2','搭乗ゲートの係員','gate','gate_agent2','ゲートの前に人がたくさん。次の都市へ出発する時間が近づいている。',[
("Attention please. Flight boarding is now open.","お知らせします。搭乗が始まりました。","*Excuse* *me*. *Can* *we* *board* *now*?","すみません。いま乗れますか。"),
("Which group are you in?","何番のグループですか。","*We* *are* *in* *group* *two*.","グループ2です。"),
("Group two will board in a few minutes. Please wait.","グループ2は数分後です。お待ちください。","*Okay*. *Is* *the* *flight* *on* *time*?","わかりました。フライトは定刻ですか。"),
("Yes, on time. You will like the view from the window.","はい、定刻です。窓からの景色を気に入りますよ。","*I* *love* *the* *view*. *I* *can't* *wait*.","景色が大好きです。待ちきれません。"),
("Group two, please come forward now. Enjoy your trip!","グループ2の方、どうぞお進みください。旅を楽しんで！","*Thank* *you*. *Goodbye*, *Nairobi*!","ありがとう。さようなら、ナイロビ！")],
[("attention","お知らせ"),("board","搭乗する"),("on time","定刻の"),("view","景色"),("come forward","前に進む")])
