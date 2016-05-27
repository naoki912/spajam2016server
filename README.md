ToDo 設計書のやつそのままコピーしただけなので綺麗に書き直す

#### データベース設計
parties(id, password)
members(id, party_id)
threads(id, party_id, type, state);
question_threads(id)
questions(id, question_thread_id, member_id, text)
coming_out_threads(id)
coming_outs(id, coming_out_thread_id, member_id, text)

users(id, group_id)
groups(id, password, number_of_people, flag)
state_groups(id, group_id, flag);
question_groups(id)
questions(id, question_group_id, user_id, text)
coming_outs_groups(id)
coming_outs(id, coming_out_group_id, user_id, text)

---
idは全て自動連番
passwordは4桁でランダム生成

ToDo 以下のAPIをv1として定義
現在のAPIからすべて書き換える

#### サーバAPI (spajam.hnron.net 157.7.53.36)
POST	/parties ? {} -> { id, members }
GET	/parties/:id ? {} -> { id, members }
POST	/threads ? { type } -> { id, type,  state }
GET	/threads/:id ? {} -> { id, party_id, state }
PUT	/threads/:id ? { id, party_id, type, is_clos }
GET	/question_threads/:thread_id ? {} -> { entries }
POST	/question_threads/:thread_id ? { entry } -> { id }
GET	/coming_out_threads/:thread_id ? {} -> { entries }
POST	/coming_out_threads/:thread_id ? { entry } -> { id }

type (question, coming_out)
state (開始状態か終了状態か)

送信受信すべてjson
レスポンスはすべてjson内に含めて送信される

METHOD URL (ARGS) (RETURN)
グループ関連
POST create_group (null) -> (user_id, group_id, password) 実装済
グループを作成してグループID(INT(4))を返す
GET join_group/<password> -> (user_id, group_id) 実装済
INTのグループIDを受け取る
POST create_question/<group_id> -> (question_group_id) 実装済
POST create_coming_out/<group_id> -> (coming_out_group_id) 実装済
POST create_none/<group_id> -> () 実装済み
質問/告白をして、最初の選択画面に戻る際に必ず実行すること

GET question/<state_group_id> -> (question_texts[[text1], [text2], … ]) 実装済
{"question_texts": [[null], [null]]}
質問一覧を取得
POST question/<state_group_id>/<user_id> (question_text) -> (null) 実装済
質問を追加
告白関連
GET coming_out/<state_group_id> -> (coming_out_texts[[text1], [text2], … ]) 実装済
告白一覧を取得
POST coming_out/<state_group_id>/<user_id> (coming_out_text) -> () 実装済
告白を追加
定期的に叩くもの
GET state_group/latest/<group_id> -> ( id, flag) 実装済
flag [question, coming_out]
質問か告白の画面で1秒間隔で叩きつづける
questionかcoming_outかのフラグと共に、そのidを返却する
何も選択されていない場合はnullを返しつづける
GET state_group/input/<group_id>/<state_group_id> (boolean)
0:false 1:true ex) {“boolean”: 1}
全員が入力し終わったか確認するために、1秒間隔で叩きつづける
こいつがtrueだったらGET question/<group_id>する

GET group/users/<group_id> -> (number_of_people)
  人数を返す
