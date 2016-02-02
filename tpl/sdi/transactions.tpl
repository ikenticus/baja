{
    "fixture": "transactions",
    "sport_name": "{{ doc['sport:content']['team-sport-content'].sport.name }}",
    "league_name": "{{ doc['sport:content']['team-sport-content']['league-content'].league.name.1['#text']|lower }}",
    "league_key": "{{ doc['sport:content']['team-sport-content']['league-content'].league.id }}",
    "teams": [
        {%- for conference in doc['sport:content']['team-sport-content']['league-content']['conference-content'] -%}
            {%- for division in conference['division-content'] -%}
                {%- for team in division['team-content'] %}
                    {
                        "team_key": "{{ team.team.id }}",
                        "transactions": [
                            {%- if team.transaction is defined -%}
                                {%- if team.transaction.date is defined %}
                                    {
                                        "date": "{{ team.transaction.date }}",
                                        "player_key": "{{ team.transaction.player.id }}",
                                        "transaction": "{{ team.transaction.details }}"
                                    }
                                {%- else -%}
                                    {%- for trans in team.transaction %}
                                        {
                                            "date": "{{ trans.date }}",
                                            "player_key": "{{ trans.player.id }}",
                                            "transaction": "{{ trans.details }}"
                                        }{% if not loop.last %},{% endif %}
                                    {%- endfor -%}
                                {%- endif -%}
                            {%- endif %}
                        ]
                    }{% if not loop.last %},{% endif %}
                {%- endfor %}{% if not loop.last %},{% endif %}
            {%- endfor %}{% if not loop.last %},{% endif %}
        {%- endfor %}{% if not loop.last %},{% endif %}
    ]
}
